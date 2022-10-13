from typing import Callable

import validators as validators

from models.Boat import Boat


class BoatsSite:
    __url: str  # Site URL
    __start_page: str  # The URL of the first page from which we will start parsing
    __boat_list_xpath: str  # xPath to list of boats
    __next_page_xpath: str | None  # xPath to next page link
    __name_xpath: str  # xPath to boat name, relative to list of all boats
    __link_xpath: str  # xPath to link to boat page, relative to list of all boats
    __price_xpath: str  # xPath to the price of the boat, relative to the list of all boats
    __loc_xpath: str  # xPath to the location of the boat, relative to the list of all boats

    __year_xpath: str  # xPath to the year the boat was built

    # A function that takes an index and returns a piece of URL,adding which to the URL __start_page we get a link
    # to the corresponding page of the list of boats
    _page_by_index: Callable[[int], str] | None

    def __init__(self, url: str, start_page: str, bl_xpath: str, name_xpath: str, link_xpath: str, price_xpath: str,
                 loc_xpath: str, np_xpath: str = None, get_page_by_index: Callable[[int], str] = None):
        self.set_url(url)
        self.set_start_page(start_page)
        self.set_boats_list_xpath(bl_xpath)
        self.set_data_xpath(name_xpath, link_xpath, price_xpath, loc_xpath)
        if not (np_xpath is None):
            self.set_next_page_xpath(np_xpath)
        else:
            self.__next_page_xpath = np_xpath
        if (np_xpath is None) and (get_page_by_index is None):
            raise TypeError("At least np_xpath or get_page must be specified")
        self._page_by_index = get_page_by_index

    def set_url(self, url: str):
        if validators.url(url):
            self.__url = url
        else:
            raise ValueError

    def get_url(self) -> str:
        return self.__url

    def set_start_page(self, start_page: str):
        if validators.url(start_page):
            self.__start_page = start_page
        else:
            raise ValueError

    def get_start_page(self) -> str:
        return self.__start_page

    def set_boats_list_xpath(self, bl_xpath: str):
        self.__boat_list_xpath = str(bl_xpath)

    def get_boats_list_xpath(self) -> str:
        return self.__boat_list_xpath

    def set_next_page_xpath(self, np_xpath):
        self.__next_page_xpath = str(np_xpath)

    def get_next_page_xpath(self):
        return self.__next_page_xpath

    def set_data_xpath(self, name_xpath: str, link_xpath: str, price_xpath: str, loc_xpath: str):
        self.__name_xpath = str(name_xpath)
        self.__link_xpath = str(link_xpath)
        self.__price_xpath = str(price_xpath)
        self.__loc_xpath = str(loc_xpath)

    def get_name_xpath(self) -> str:
        return self.__name_xpath

    def get_link_xpath(self) -> str:
        return self.__link_xpath

    def get_price_xpath(self) -> str:
        return self.__price_xpath

    def get_loc_xpath(self) -> str:
        return self.__loc_xpath

    def get_next_page_link(self, tree=None, index: int = None) -> str | None:
        """
            This function returns a link to the next page of the product list.

            If the tree parameter is passed, then the function takes the parsed page and looks for
            a link to the next one using __next_page_xpath. Otherwise, if an index is passed,
            then the link to the next page will be calculated using the _page_by_index function
            (link = __start_page + page_by_index(index)).

            Args:
               tree: This is a parsed page(HTML element tree).
               index: This is the index of the page (an integer greater than or equal to 0).

            Returns:
               This function returns a link to the next page.
        """
        if not (tree is None):
            if not (self.__next_page_xpath is None):
                next_page = tree.xpath(self.__next_page_xpath)
                # print("LINK: ", next_page)
                if len(next_page) > 0:
                    next_page = str(next_page[0])
                    if not next_page.startswith(self.__url):
                        next_page = self.__url + next_page
                else:
                    next_page = None
                return next_page
            else:
                raise TypeError("The __next_page_xpath is not defined for this site")
        elif not (index is None):
            if not (self._page_by_index is None):
                return self.__start_page + self._page_by_index(index)
            else:
                raise TypeError("The _page_by_index() function is not defined for this site")
        else:
            raise TypeError("The get_next_page_link function is missing a required argument tree or index")

    def find_boats(self, tree) -> list[Boat]:
        """
            This function takes a parsed page and returns a list of all found boats.

            Args:
                tree: This is a parsed page(HTML element tree).

            Returns:
                This function returns a list of Boat class objects parsed on this page.
        """
        li_in_boat_list = tree.xpath(self.__boat_list_xpath)
        boats_list = []
        for li_ in li_in_boat_list:
            title = str(li_.xpath(self.__name_xpath)[0])
            words = title.split()
            boat_name = " "
            for w in words:
                boat_name += w + "  "
            boat_name = boat_name[:-1]

            boat_link = str(li_.xpath(self.__link_xpath)[0])
            boat_link = self.__url + str(boat_link) if not boat_link.startswith(self.__url) else boat_link

            boat_price = li_.xpath(self.__price_xpath)
            boat_price = str(boat_price[0]) if len(boat_price) > 0 else ""

            boat_location = li_.xpath(self.__loc_xpath)
            boat_location = str(boat_location[0]) if len(boat_location) > 0 else ""

            boats_list.append(Boat(boat_name, boat_price, boat_link, boat_location))
        return boats_list
