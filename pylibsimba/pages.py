# from __future__ import annotations
from typing import Optional


class PagedResponse:
    """Wrapper for paged responses"""

    def __init__(self, data, url, simba: 'Simbachain'):
        self.url = url
        self._count = data['count']
        self._next_page = data['next']
        self._previous_page = data['previous']
        self.results = data['results']
        self.simba = simba

    def next(self): # -> Optional[PagedResponse]:
        """
        Grab the next page

        Returns:
            PagedResponse for the next page, or None if not available
        """
        if not self._next_page:
            return None
        return self.simba.send_transaction_request(self._next_page)

    def previous(self): # -> Optional[PagedResponse]:
        """
        Grab the previous page

        Returns:
            PagedResponse for the next page, or None if not available
        """
        if not self._previous_page:
            return None
        return self.simba.send_transaction_request(self._previous_page)

    def data(self) -> dict:
        """
        Returns the actual data

        Returns:
            Dict of all the results
        """
        return self.results

    def count(self) -> int:
        """
        Returns:
            The number of results available
        """
        return self._count

    def current_page(self):
        """
        Returns:
            The current page number
        """
        return self.url['searchParams'].get('page')

    def next_page(self):
        """
        Returns:
            The next page number
        """
        return self._next_page

    def previous_page(self):
        """
        Returns:
            The previous page number
        """
        return self._previous_page
