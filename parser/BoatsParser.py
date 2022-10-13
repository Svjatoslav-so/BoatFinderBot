import time

from models.Boat import Boat
from parser.BoatsSiteProtocol import BoatsSiteProtocol

from parser.Parser import Parser


class BoatsParser(Parser):

    def parse(self, site: BoatsSiteProtocol, res_list: list = None) -> list[Boat]:
        """
            This function returns a list of all the boats it was able to find on this site.

            If a res_list argument is passed, then the result will also be written to it (used for multithreading).

            Args:
                site: This is the site to be parsed (must be BoatsSiteProtocol compliant).
                res_list: This is a list, if one was passed, then the result will be written to it.

            Returns:
                This function returns a list of objects of type Boat.
        """
        # start = time.perf_counter()
        boats = self._get_all_boats(site, site.get_start_page())
        # end = time.perf_counter()
        # print("BOATS_PARSER: ", end - start)
        if not(res_list is None):
            res_list.extend(boats)
        return boats

    def _get_all_boats(self, site: BoatsSiteProtocol, start_page: str,
                       boats_list: list[Boat] | None = None, index: int = 0) -> list[Boat]:
        """
        This function recursively traverse all pages of the site and collects data in a list.

        Args:
            site: This is the site to be parsed (must be BoatsSiteProtocol compliant).
            start_page: This is a link to the start page where parsing starts.
            boats_list: This is a list of parsed objects.
            index: This is the recursion depth index (= number of parsed pages).

        Returns:
            This function returns a list of objects of class Boat.
        """
        if boats_list is None:
            boats_list = []
        # print("start ", index, end=" ")
        index += 1
        tree = self.get_tree(start_page)
        boats_list = boats_list + site.find_boats(tree)
        if not (tree is None):
            next_p = site.get_next_page_link(tree)
            # print("next ", next_p)
            if not (next_p is None):
                boats_list = self._get_all_boats(site, next_p, boats_list, index)
            return boats_list

        else:
            return boats_list
