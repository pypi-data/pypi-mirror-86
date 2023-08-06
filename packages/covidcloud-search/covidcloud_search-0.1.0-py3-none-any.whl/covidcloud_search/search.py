import requests

from typing import List


def ga4gh_search(url: str, query: str) -> List[List[str]]:

    """
    Returns list formatted ga4gh search response from a url and query

    :param url: API url
    :param query: SQL query
    :return: List formated json response

    """

    response = requests.post(url, json=query)
    response_url = response.json()['pagination']

    data = []
    while response_url:
        response = requests.get(response_url['next_page_url'])
        data += response.json()['data']
        response_url = response.json()['pagination']

    return data
