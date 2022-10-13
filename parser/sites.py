from parser.BoatsSite import BoatsSite

# boatshop24@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
boatshop24_url = "https://www.boatshop24.com"
# boatshop24_start_page = "https://www.boatshop24.com/boats-for-sale/class-sailing-boats/page-40/"
boatshop24_start_page = "https://www.boatshop24.com/boats-for-sale/class-sailing-boats/"
boatshop24_li_list = '//*[@id="right-content"]/div[2]/ol/li[@data-listing-id]'
boatshop24_next_page = "//ul[@class='pagination']/li/a[@class='next']/@href"
boatshop24_name = 'div/div[2]/div[1]/div[1]/h2/text()'
boatshop24_link = 'div/div[2]/div[1]/div[@class = "name"]/a/@href'
boatshop24_price = 'div/div[2]/div[1]/div[@class = "price"]/text()'
boatshop24_location = 'div/div[2]/div[1]/div[@class = "location"]/text()'

BOATSHOP24 = BoatsSite(boatshop24_url, boatshop24_start_page, boatshop24_li_list, boatshop24_name,
                       boatshop24_link, boatshop24_price, boatshop24_location, boatshop24_next_page)


# boat24@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def pager(index: int) -> str:
    """This function takes a page index and returns a string (end of URL) for the "Boat24" site"""
    url_page = ""
    if 200 > index > 1:
        url_page += "?page=" + str((index - 1) * 2) + "0"
    elif index > 200:
        url_page += "BREAK"
    return url_page


boat24_url = "https://www.boat24.com/en/"
boat24_start_page = "https://www.boat24.com/en/sailboats/"
boat24_li_list = '//*[@id="sticky-header-trigger"]/div/ul/li/div[@data-link]'
boat24_next_page = "//div[@class='pagination l-mt-64 l-mb-64']/" \
                   "span[contains(text(),'Next page')]/@data-link"
boat24_name = 'div[@class="blurb__main"]/h3[@class="blurb__title"]/a/text()'
boat24_link = 'div[@class="blurb__main"]/h3[@class="blurb__title"]/a/@href'
boat24_price = 'aside[@class="blurb__side"]/p[@class="blurb__price"]/text()'
boat24_location = 'div[@class="blurb__main"]/p[@class="blurb__location"]/text()'

BOAT24 = BoatsSite(boat24_url, boat24_start_page, boat24_li_list, boat24_name, boat24_link,
                   boat24_price, boat24_location, boat24_next_page, pager)

# yachtworld@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
yachtworld_url = "https://www.yachtworld.com/"
yachtworld_start_page = "https://www.yachtworld.com/boats-for-sale/type-sail/"
yachtworld_li_list = '//div[@class="listings-container"]/a'
# yachtworld_next_page = "//div[@class='search-page-nav']/a[@class='icon-chevron-right ']/@href"
yachtworld_next_page = "//div[@class='search-page-nav']/a[@class='active']//following-sibling::a[2]/@href"
yachtworld_name = 'div[contains(@class,"row listing-card")]/div[@class="listing-card-information"]/h2/text()'
yachtworld_link = '@href'
yachtworld_price = 'div[contains(@class,"row listing-card")]/div[@class="listing-card-information"]/' \
                   'div[@class="price"]//text()'
yachtworld_location = 'div[contains(@class,"row listing-card")]/div[@class="listing-card-information"]/' \
                      'div[@class="listing-card-location"]/text()'
YACHTWORLD = BoatsSite(yachtworld_url, yachtworld_start_page, yachtworld_li_list, yachtworld_name,
                       yachtworld_link, yachtworld_price, yachtworld_location, yachtworld_next_page,
                       lambda index: "?page=" + str(index) if index > 0 else '')
