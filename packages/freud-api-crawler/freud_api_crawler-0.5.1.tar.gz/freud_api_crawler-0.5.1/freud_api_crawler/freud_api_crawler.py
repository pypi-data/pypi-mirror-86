import os
import json
import time
from collections import defaultdict

import requests

FRD_API = os.environ.get('FRD_API', 'https://www.freud-edition.net/jsonapi/')
FRD_USER = os.environ.get('FRD_USER', False)
FRD_PW = os.environ.get('FRD_PW', False)

SAMPLE_MANIFESTATION = os.path.join(
    os.path.dirname(__file__),
    "fixtures",
    "manifestation.json"
)
SAMPLE_MANIFESTATION_PAGE = os.path.join(
    os.path.dirname(__file__),
    "fixtures",
    "manifestation_seite.json"
)


class FrdClient():

    """Main Class to interact with freud.net-API """

    def list_endpoints(self):
        """ returns a list of existing API-Endpoints
        :return: A PyLobidPerson instance
        """
        if self.authenticated:
            r = requests.get(
                self.endpoint, auth=(self.user, self.pw)
            )
            result = r.json()
            d = defaultdict(list)
            for key, value in result['links'].items():
                url = value['href']
                node_type = url.split('/')[-2]
                d[node_type].append(url)
            return d
        else:
            return {}

    # def crawl_endpoint(self, url_part, important_values):
    #     """ method for iterating over drupal-endpoints
    #     :param url_part: specific API endpoint, e.g. 'werk' -> {drupalbase}/jsonapi/node/{url_part}
    #     :type gnd_id: str
    #     :param important_values: simple attribute names, e.g. ['title', 'field_year']
    #     :type user: list
    #
    #     :return: print things
    #     """
    #
    #     url = f"{self.endpoint}node/{url_part}?page[limit]={self.page_size}"
    #     next_page = True
    #     counter = 0
    #     auth = ()
    #     while next_page:
    #         print(url)
    #         response = requests.get(url, auth=(self.user, self.pw))
    #         result = response.json()
    #         links = result['links']
    #         for y in result['data']:
    #             self_uri = y['links']['self']['href']
    #             print(self_uri)
    #             attributes = y['attributes']
    #             for val in important_values:
    #                 print(attributes[val])
    #         if links.get('next', False):
    #             url = links['next']['href']
    #         else:
    #             next_page = False
    #         counter += 1
    #         print(counter)
    #         if self.limit > 0:
    #             if counter >= self.limit:
    #                 next_page = False
    #         time.sleep(self.sleep)

    def __init__(
        self,
        endpoint=FRD_API,
        user=FRD_USER,
        pw=FRD_PW,
        page_size=10,
        limit=10,
        sleep=0.5
    ):

        """ initializes the class

        :param endpoint: The API Endpoint
        :type gnd_id: str
        :param user: The API user name
        :type user: str
        :param pw: The user's password
        :type pw: str
        :param page_size: Default page size of api-return -> &page[limit]={self.limit}
        :type pw: int
        :param limit: After how many next-loads the loop should stop
        :type pw: int
        :param sleep: Time to pause crawling loop
        :type pw: float

        :return: A FrdClient instance
        """
        super().__init__()
        self.endpoint = endpoint
        self.user = user
        self.pw = pw
        self.page_size = page_size
        self.limit = limit
        self.sleep = sleep
        if self.pw and self.user:
            self.authenticated = True
        else:
            print("no user and password set")
            self.authenticated = False


class FrdManifestation(FrdClient):

    """class to deal with Manifestations
    :param manifestation_id: The hash ID of a Manifestation Node
    :type gnd_id: str

    :return: A FrdManifestation instance
    """

    def get_manifest(self):
        """ returns the manifest json as python dict

        :return: a Manifestation representation
        """
        r = requests.get(
            self.manifestation_endpoint, auth=(self.user, self.pw)
        )
        status_code = r.status_code
        if status_code != 200:
            print(
                f"could not access {self.manifestation_endpoint} because\
                of {status_code}, using local sample"
            )
            with open(SAMPLE_MANIFESTATION) as json_file:
                result = json.load(json_file)
        else:
            result = r.json()
        return result

    def get_pages(self):
        """ method returning related page-ids/urls

        :returns a list of dicts {'id': 'hash-id', 'url': 'page_url'}
        """
        page_list = []
        for x in self.manifestation['data']['relationships']['field_seiten']['data']:
            node_type = x['type'].split('--')[1]
            page = {
                'id': x['id'],
                'url': f"{self.endpoint}node/{node_type}/{x['id']}"
            }
            page_list.append(page)
        return page_list

    def __init__(
        self,
        manifestation_id=None
    ):
        super().__init__()
        self.manifestation_id = manifestation_id
        self.manifestation_endpoint = f"{self.endpoint}node/manifestation/{manifestation_id}"
        self.manifestation = self.get_manifest()
        self.man_attrib = self.manifestation['data']['attributes']
        for x in self.man_attrib.keys():
            value = self.man_attrib[x]
            if isinstance(value, dict):
                for y in value.keys():
                    dict_key = f"{x}__{y}"
                    setattr(self, f"md__{dict_key}", value[y])
            else:
                setattr(self, f"md__{x}", value)
        self.meta_attributes = [x for x in dir(self) if x.startswith('md__')]
        self.pages = self.get_pages()
        self.page_count = len(self.pages)
