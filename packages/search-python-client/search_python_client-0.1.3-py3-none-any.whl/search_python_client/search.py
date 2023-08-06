import os
import pandas as pd
import requests

from typing import List


class DrsClient:
    """
    DRS client for DNAstack's DRS API's.

    :param url: Base url to search on

    :Example:
        from search_python_client.search import DrsClient\n
        url = 'https://drs.covidcloud.ca/ga4gh/drs/v1/'\n
        drs_client = DrsClient(url=url)

    """

    def __init__(self, url: str):
        self.url = url

    def __str__(self):
        return f'DrsClient(url={self.url})'

    def __repr__(self):
        return f'DrsClient(url={self.url})'

    def _get(self, url: str) -> dict:
        """
        Executes get request and returns dict formatted json response

        :param url: Url to search on
        :returns: dict formatted json response
        :raises HTTPError: If response != 200

        """
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def object_info(self, object_id: str) -> pd.DataFrame:
        """
        List all info associated with object.

        :param object_info: Object id of choice
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return pd.DataFrame(
            self._get(os.path.join(self.url, 'objects', object_id))
        )


class SearchClient:
    """
    Search client for DNAstack's search API's.

    :param url: Base url to search on

    :Example:
        from search_python_client.search import SearchClient\n
        url = 'https://ga4gh-search-adapter-presto-covid19-public.prod.dnastack.com/'\n
        search_client = SearchClient(url=url)

    """

    def __init__(self, url: str):
        self.url = url

    def __str__(self):
        return f'SearchClient(url={self.url})'

    def __repr__(self):
        return f'SearchClient(url={self.url})'

    def _get(self, url: str) -> dict:
        """
        Executes get request and returns dict formatted json response

        :param url: Url to search on
        :returns: dict formatted json response
        :raises HTTPError: If response != 200

        """
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _get_paginated(self, url: str, pages: int) -> List[dict]:
        """
        Executes get request for paginated responses

        :param url: Url to search on
        :param pages: Number of pages to return
        :returns: List of dict formatted json responses
        :raises HTTPError: If response != 200

        """
        base_name = os.path.basename(url)
        json_responses = []
        json_response = self._get(url)
        json_responses += json_response[base_name]

        pages_counter = 1
        while 'pagination' in json_response and pages_counter < pages:
            try:
                json_response = self._get(
                    json_response['pagination']['next_page_url']
                    )
            except KeyError:
                return json_responses
            json_responses += json_response[base_name]
            pages_counter += 1

        return json_responses

    def _post(self, url: str, json: dict) -> dict:
        """
        Executes post request and returns dict formatted json response

        :param url: Url to search on
        :param json:  Dict formatted json query
        :returns: dict formatted json response
        :raises HTTPError: If response != 200

        """
        response = requests.post(url, json={'query': json})
        response.raise_for_status()
        return response.json()

    def _post_paginated(self, url, json, pages):
        """
        Executes post request for paginated responses

        :param url: Url to search on
        :param json:  Dict formatted json query
        :param pages: Number of pages to return
        :returns: List of dict formmated json responses
        :raises HTTPError: If response != 200

        """
        json_responses = []
        json_response = self._post(url, json=json)
        json_responses += json_response['data']

        pages_counter = 1
        while 'pagination' in json_response and pages_counter < pages:
            try:
                json_response = self._get(
                    json_response['pagination']['next_page_url']
                    )
            except KeyError:
                return json_responses
            json_responses += json_response['data']
            pages_counter += 1

        return json_responses

    def list_tables(self, pages: int = 100) -> pd.DataFrame:
        """
        List all tables associated with the url.

        :param pages: Number of pages to return. Defaults to 100
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return pd.DataFrame(
            self._get_paginated(
                os.path.join(self.url, 'tables'), pages
                )
        )

    def table_info(self, table_name: str) -> pd.DataFrame:
        """
        List all info associated with table_name.

        :param table_name: Table name of choice
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return pd.DataFrame(
            self._get(os.path.join(self.url, 'table', table_name, 'info'))
        )

    def table_data(self, table_name: str, pages: int = 100) -> pd.DataFrame:
        """
        Get all data associated with table_name.

        :param table_name: Table name of choice
        :param pages: Number of pages to return. Defaults to 100
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return pd.DataFrame(
            self._get_paginated(
                os.path.join(self.url, 'table', table_name, 'data'), pages
                )
        )

    def search_table(self, query: str, pages: int = 100) -> pd.DataFrame:
        """
        Executes an SQL query on table of choice and returns associated data.

        :param table_name: Table name of choice
        :param pages: Number of pages to return. Defaults to 100
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        :Example: query = 'SELECT * FROM coronavirus_dnastack_curated.covid_cloud_production.sequences_view LIMIT 1000'

        """
        return pd.DataFrame(
            self._post_paginated(
                os.path.join(self.url, 'search'), query, pages
            )
        )
