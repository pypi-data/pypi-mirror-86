"""
    base_es.py
    -----------------------------------------
    This module contains Abstract base classes for elastic search
"""

__author__ = "Allan Chepkoy"
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Any

PAGE_INDEX = 0
INDEX_STRING = ""


class BaseElasticSearch(metaclass=ABCMeta):
    """
    The BaseElasticSearch is an interface for all the proxy clients
    available in the search service
    """

    @abstractmethod
    def get_table_results(
        self,
        *,
        query_term: str,
        page_index: int = PAGE_INDEX,
        index: str = INDEX_STRING
    ):

        """
        Fetches the table search results.

        :param *:
        :param query_term: Search term which should be a string
        :param page_index: The number of pages to index which should be a integer
        :param index: Index page should be a string
        :return: SearchTableResult


        """

    @abstractmethod
    def create_document(self, *, data: List[Dict[str, Any]], index: str = "") -> str:
        """
        Creates a document.

        :param *:
        :param data: Data to create the document
        :param index: Index page should be a string
        :return: A string of

        """
