from typing import Any

import requests
from lxml import html

from models.Boat import Boat
from parser.BoatsSiteProtocol import BoatsSiteProtocol


class Parser:

    def parse(self, site: BoatsSiteProtocol, result_boats_list: list | None = None) -> list[Boat]:
        """
            This function returns a list of all the boats it was able to find on this site.

            If a result_boats_list argument is passed, then the result will also be written to it (used for multithreading).

            Args:
                site: This is the site to be parsed (must be BoatsSiteProtocol compliant).
                result_boats_list: This is a list, if one was passed, then the result will be written to it.

            Returns:
                This function returns a list of objects of type Boat.
        """
        pass

    @staticmethod
    def get_tree(page_url: str) -> Any | None:
        """
            This function takes a link to a page and returns an HTML tree (DOM).

            Args:
                page_url: This is a link to a page.

            Returns:
                This function returns the parsed page as a tree of  HTML elements.
        """
        response = requests.get(page_url)

        print(f"LINK: {page_url} CODE: {response.status_code}")

        if response.status_code == 200:
            tree = html.fromstring(response.text)
        else:
            tree = None

        return tree
