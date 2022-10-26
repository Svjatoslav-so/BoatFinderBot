import time
from threading import Thread
from typing import Any, Optional
from bs4 import BeautifulSoup

import requests

from models.Boat import Boat

boat24_URL = "https://www.boat24.com/en/sailboats/"


def get_page(page_url: str) -> Any | None:
    """
        This function takes a link to a page and returns a page.

        Args:
            page_url: This is a link to a page.

        Returns:
            This function returns the page.
    """

    try:
        response = requests.get(page_url, timeout=4)
    except:
        return None

    print(f"LINK: {page_url} CODE: {response.status_code}")
    if response.status_code == 200:
        page = response.text
    else:
        page = None
    return page


def parse_boat_page(link: str, boats: list):
    page = get_page(link)
    if page is None:
        return None
    b_soup = BeautifulSoup(page, "html.parser")
    boat = {}

    boat.update({"link": link})
    photo = b_soup.find("picture")
    if not (photo is None):
        photo = photo.find("img")["src"]
        # print("Photo", photo)
        boat.update({"photo": photo})
    if b_soup.find("header", class_="heading") is None:
        with open("log.txt", "a") as f:
            f.write(f"link: {link}\n")
        return None

    title = b_soup.find("header", class_="heading").contents[1]
    # print("title", title)
    boat.update({"title": title.get_text()})

    boat_type = b_soup.find("header", class_="heading").contents[0]
    # print("boat_type", boat_type.get_text())
    boat.update({"boat_type": boat_type.get_text()})

    price = b_soup.find("div", class_="contact-box__price-section")
    if not (price is None):
        price = price.find("div", class_="l-hide--sm-d")
        # print(price)
        boat.update({"price": price.get_text()})

    location = b_soup.find("div", id="location")
    if not (location is None):
        location = location.find("p", class_="text")
        # print(location)
        boat.update({"location": location.get_text()})

    boat.update({"other_param": {}})
    specs_li = b_soup.find("div", id="specs").find_all("li")
    for li in specs_li:
        # print(li)
        key = li.find("span", class_="list__key")
        key = key.string if not (key is None) else key
        if not (key is None):
            if key.count("Year Built") > 0:
                boat.update({"year": li.span.get_text()})
            elif key.count("Length x Beam") > 0:
                # print("Length x Beam", li.span.get_text())
                boat.update({"length x beam": li.span.get_text()})
            elif key.count("Draught") > 0:
                # print("Draught", li.span.get_text())
                boat.update({"draft": li.span.get_text()})
            elif key.count("Material") > 0:
                # print("Material", li.span.get_text())
                boat.update({"material": li.span.get_text()})
            elif key.count("Fuel Type") > 0:
                # print("Fuel Type", li.span.get_text())
                boat.update({"fuel_type": li.span.get_text()})
            elif key.count("CE Design Category") > 0:
                # print("CE Design Category", li.span.get_text())
                boat.update({"CE_design_category": li.span.get_text()})
            else:
                # print(key, " >>> ", li.span.get_text())
                boat["other_param"].update({key: li.span.get_text()})

    description = b_soup.find("div", id="description")
    if not (description is None):
        description = description.find("div", class_="content--readmore")
        # print(description.get_text())
        boat.update({"description": description.get_text()})

    res_boat = toBoat(boat)
    boats.append(res_boat)


def parse_boats_page(page):
    soup = BeautifulSoup(page, "html.parser")
    all_boats_in_page = soup.findAll("div", class_="blurb")
    print("div ", len(all_boats_in_page))
    links_to_boat_pages = []
    for boat in all_boats_in_page:
        links_to_boat_pages.append(boat.get("data-link"))
        # print(boat)
    print("link ", len(links_to_boat_pages))
    # print(links_to_boat_pages)

    boats = []
    threads = []
    for link in links_to_boat_pages:
        t = Thread(target=parse_boat_page, args=(link, boats))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return boats


def get_url_by_index(index: int) -> str:
    if index <= 0:
        return boat24_URL
    else:
        return boat24_URL + f"?page={index * 2}0"


def parse_by_step(boats_list: list, start: int, step: int) -> list:
    boats = []
    next_page = start
    print("T: ", start)
    page = get_page(get_url_by_index(next_page))
    while not (page is None):
        new_boats = parse_boats_page(page)
        boats.extend(new_boats)
        if len(new_boats) < 4:
            print(f"T: {start} Len: {len(new_boats)} ")
            break
        next_page += step
        print("T: ", start)
        page = get_page(get_url_by_index(next_page))
    boats_list.extend(boats)
    with open("log_thread.txt", "a") as f:
        f.write(f"TREAD: {start} END\n")
    return boats


def parse(threads_num: int = 10, res_list: list = None):
    boats_list = []
    threads = []
    for i in range(threads_num):
        p_t = Thread(target=parse_by_step, args=(boats_list, i, threads_num))
        threads.append(p_t)
        p_t.start()
    for p_t in threads:
        p_t.join()
    if not (res_list is None):
        res_list.extend(boats_list)
    return boats_list


def get_price(price: str) -> str:
    if not (price is None) and price.count("EUR") > 0:
        res = ""
        for s in price[price.find("EUR"):]:
            if s.isdigit():
                res += s

        return res
    else:
        return "None"


def get_length_beam(length_beam: str) -> Optional[tuple[str, str]]:
    length = beam = None
    if not (length_beam is None):
        length = beam = ""
        is_length = True
        for s in length_beam:
            if s.isdigit() or s == ".":
                if is_length:
                    length += s
                else:
                    beam += s
            elif s == "x":
                is_length = False
    return length, beam


def get_draft(draft: str) -> Optional[str]:
    if not(draft is None):
        res = ""
        for s in draft:
            if s.isdigit() or s == ".":
                res += s
        return res
    else:
        return None


def toBoat(boat: dict) -> Boat:
    price_num = get_price(boat.get("price"))
    length, beam = get_length_beam(boat.get("length x beam"))
    draft = get_draft(boat.get("draft"))
    return Boat(boat.get("title"), boat.get("price"), price_num, boat.get("link"), boat.get("location"),
                boat.get("year"), length, beam, draft, boat.get("material"), boat.get("fuel_type"),
                str(boat.get("other_param")), boat.get("description"), boat.get("photo"),
                boat.get("CE_design_category"), boat.get("boat_type"))


if __name__ == '__main__':
    with open("log_thread.txt", "w") as fw:
        pass

    with open("log.txt", "w") as fw_:
        pass

    boats_li = []
    time_start = time.time()
    print("LEN: ", len(parse(10, boats_li)))
    time_end = time.time()
    print("boats ", len(boats_li))
    print("TIME: ", time_end - time_start)

    for b in boats_li:
        # pass
        print(b)
    # print(get_price("DKK 229.000,-apx. EUR 30.791,-Basis for Negotiation / EU taxes paid"))
    # print(get_length_beam("11.03 m x 3.18 m"))
    # l, b = get_length_beam("11.03 m x 3.18 m")
    # print(float(l))
    # print(float(b))
