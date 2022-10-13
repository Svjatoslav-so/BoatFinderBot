from abc import abstractmethod
from typing import Protocol, Callable, Any

from models.Boat import Boat


class BoatsSiteProtocol(Protocol):
    __url: str  # Site url
    __start_page: str  # The URL of the first page from which we will start parsing
    __boat_list_xpath: str  # xPath to list of boats
    __next_page_xpath: str  # xPath to next page link
    __name_xpath: str  # xPath to boat name, relative to list of all boats
    __link_xpath: str  # xPath to link to boat page, relative to list of all boats
    __price_xpath: str  # xPath to the price of the boat, relative to the list of all boats
    __loc_xpath: str  # xPath to the location of the boat, relative to the list of all boats

    # A function that takes an index and returns a piece of URL,adding which to the URL __start_page we get a link
    # to the corresponding page of the list of boats
    _page_by_index: Callable[[int, ...], str]

    @abstractmethod
    def __init__(self, url: str, start_page: str, bl_xpath: str, name_xpath: str, link_xpath: str, price_xpath: str,
                 loc_xpath: str, np_xpath: str, get_page_by_index: Callable[[int, Any], str]):
        raise NotImplementedError

    @abstractmethod
    def set_url(self, url: str):
        raise NotImplementedError

    @abstractmethod
    def get_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_start_page(self, start_page: str):
        raise NotImplementedError

    @abstractmethod
    def get_start_page(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_boats_list_xpath(self, bl_xpath: str):
        raise NotImplementedError

    @abstractmethod
    def get_boats_list_xpath(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_next_page_xpath(self, np_xpath: str):
        raise NotImplementedError

    @abstractmethod
    def get_next_page_xpath(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_data_xpath(self, name_xpath: str, link_xpath: str, price_xpath: str, loc_xpath: str):
        raise NotImplementedError

    @abstractmethod
    def get_name_xpath(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_link_xpath(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_price_xpath(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_loc_xpath(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_next_page_link(self, tree=None, index: int = None) -> str | None:
        """
            This function returns a link to the next page of the product list.

            If the tree parameter is passed, then the function takes the parsed page and looks for
            a link to the next one using __next_page_xpath. Otherwise, if an index is passed,
            then the link to the next page will be calculated using the _page_by_index function.

            Args:
               tree: This is a parsed page(HTML element tree).
               index: This is the index of the page (an integer greater than or equal to 0).

            Returns:
               This function returns a link to the next page.
        """
        raise NotImplementedError

    @abstractmethod
    def find_boats(self, tree) -> list[Boat]:
        """
            This function takes a parsed page and returns a list of all found boats.

            Args:
                tree: This is a parsed page(HTML element tree).

            Returns:
                This function returns a list of Boat class objects parsed on this page.
        """
        raise NotImplementedError
