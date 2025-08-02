from rest_framework.pagination import PageNumberPagination

"""
Custom pagination class to standardize paginated API responses.

This module defines:
- StandardResultsSetPagination: A PageNumberPagination subclass with configurable page size parameters.
"""


class StandardResultsSetPagination(PageNumberPagination):
    """
    Provides pagination using page number style with default and maximum limits.

    Attributes:
        page_size (int): Default number of items per page (default=2).
        page_size_query_param (str): Query parameter to adjust page size (default='page_size').
        max_page_size (int): Maximum allowable page size (default=1000).

    Usage:
        Add StandardResultsSetPagination to a view or viewset's pagination_class to enable.
    """

    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 1000
