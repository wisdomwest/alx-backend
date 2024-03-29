#!/usr/bin/env python3
'''pagination'''

import csv
from typing import List, Tuple


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    @staticmethod
    def index_range(page: int, page_size: int) -> Tuple[int, int]:
        '''return a tuple of size two containing a start index and an end index
        corresponding to the range of indexes to return in a list for those
        particular pagination parameters.
        Page numbers are 1-indexed, i.e. the first page is page 1'''

        return ((page * page_size) - page_size, page * page_size)

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''takes two integer arguments page with default value 1 and page_size
        with default value 10'''
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        range = self.index_range(page, page_size)
        start = range[0]
        end = range[1]

        return self.dataset()[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        '''Implement a get_hyper method that takes same arguments as get_page
        and returns a dictionary containing the following key-value pairs:
        page_size: the length of the returned dataset page
        page: the current page number
        data: the dataset page (equivalent to return from previous task)
        next_page: number of the next page, None if no next page
        prev_page: number of the previous page, None if no previous page
        total_pages: the total number of pages in the dataset as an integer'''

        data = self.get_page(page, page_size)
        total_pages = len(self.dataset()) / page_size
        if total_pages % 1 != 0:
            total_pages = int(total_pages) + 1
        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if page < total_pages else None,
            'prev_page': page - 1 if page > 1 else None,
            'total_pages': int(total_pages)
        }
