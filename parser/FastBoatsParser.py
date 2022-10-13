import time
from threading import Thread

from models.Boat import Boat
from parser.BoatsSiteProtocol import BoatsSiteProtocol
from parser.Parser import Parser


class FastParser(Parser):
    __threads_num: int  # number of threads used for parsing

    def __init__(self, threads_num: int):
        self.set_threads_num(threads_num)

    def set_threads_num(self, threads_num: int):
        if (type(threads_num) == int) and (threads_num > 0):
            self.__threads_num = threads_num
        else:
            self.__threads_num = 5

    def parse(self, site: BoatsSiteProtocol, res_list: list = None) -> list[Boat]:
        """
            This function returns a list of all the boats it was able to find on this site.

            If a res_list argument is passed, then the result will also be written to it (used for multithreading).
            This function parses the entire site into several threads (equal to __threads_num),
            each thread takes the first page for itself and then goes with a step equal to the number of threads.

            Args:
                site: This is the site to be parsed (must be BoatsSiteProtocol compliant).
                res_list: This is a list, if one was passed, then the result will be written to it.

            Returns:
                This function returns a list of objects of type Boat.
        """
        # start = time.perf_counter()
        boats = []
        threads = []
        for i in range(self.__threads_num):
            print(f"I {i}")
            p_t = Thread(target=self._parse_by_step, args=(site, boats, i, self.__threads_num))
            threads.append(p_t)
            p_t.start()
        for p_t in threads:
            p_t.join()
        # end = time.perf_counter()
        # print("PARSE: ", end - start)
        if not (res_list is None):
            res_list.extend(boats)
        return boats

    def _parse_by_step(self, site: BoatsSiteProtocol, boats_list: list, start: int, step: int):
        """
            This is a helper function, it parses the pages of the site with the specified step.

            The result of parsing is added to the list boats_list.
            This function for parsing the page itself allocates a separate thread.

            Args:
                site: This is the site to be parsed (must be BoatsSiteProtocol compliant).
                boats_list: This is a list of results common to all threads, the result of parsing is added here.
                start: This is the index of the page to start parsing from.
                step: This is the step with which the function will iterate through the pages of the site
                      starting from start.
        """
        find_threads = []
        page_index = start
        while True:
            next_page = site.get_next_page_link(index=page_index)
            print(f"T: {start} NEXT: {next_page}")
            tree = self.get_tree(next_page)
            if not (tree is None):
                t = Thread(target=self._find_boats_on_page, args=(site, boats_list, tree))
                t.start()
                find_threads.append(t)
                page_index += step
            else:
                break
        for t in find_threads:
            t.join()

    @staticmethod
    def _find_boats_on_page(site, boat_list, page_tree):
        """
            This function parses the html passed to it and adds the resulting objects to the passed list of objects.

            This is a helper function, it is needed to move this action to a separate thread.

        Args:
            site: This is an BoatsSiteProtocol object required for parsing html.
            boat_list: This is the list to which the result will be added.
            page_tree: This is a parsed page(HTML element tree).
        """
        boat_list.extend(site.find_boats(page_tree))
