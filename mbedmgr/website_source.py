import requests
import bs4
import threading
import lxml
import typing
import uuid
import time
import json

class WebpageData(typing.TypedDict):
    """TODO"""

    text: str

class WebsiteSource:
    """TODO"""

    def __init__(self):
        self._data = {}
        self._preprocess = None
        self._segment = None
        self._embed = None

    @property
    def data(self) -> typing.Dict[str, WebpageData]:
        return self._data

    def get_pages_from_sitemap(self, sitemap_url: str) -> None:
        response = requests.get(sitemap_url)
        root = lxml.etree.fromstring(response.content)
        namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.xpath('//sitemap:loc', namespaces=namespaces)]
        for url in urls:
            self._data[url] = {}

    def scrape(self) -> None:
        threads = []
        for url in self._data:
            thread_id = str(uuid.uuid4())
            thread = threading.Thread(target=self._scrape, name=thread_id, args=(url,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def _scrape(self, url: str) -> None:
        response = requests.get(url)
        if not response.ok:
            return
        self._data[url] = {
            'text': response.text,
            'type': response.headers.get('Content-Type')
        }

    def preprocess(self) -> None:
        if self._preprocess is None:
            print('preprocess() has no effect because a handler was not set.')
            return
        threads = []
        for url in self._data:
            thread_id = str(uuid.uuid4())
            # TODO: It's not necessary to give them access to the whole data object.
            thread = threading.Thread(target=self._preprocess, name=thread_id, args=(url,self._data,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def segment(self) -> None:
        if self._segment is None:
            print('segment() has no effect because a handler was not set.')
            return
        threads = []
        for url in self._data:
            thread_id = str(uuid.uuid4())
            # TODO: It's not necessary to give them access to the whole data object.
            thread = threading.Thread(target=self._segment, name=thread_id, args=(url,self._data,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def embed(self) -> None:
        if self._embed is None:
            print('embed() has no effect because a handler was not set.')
            return
        threads = []
        for url in self._data:
            thread_id = str(uuid.uuid4())
            # TODO: It's not necessary to give them access to the whole data object.
            thread = threading.Thread(target=self._embed, name=thread_id, args=(url,self._data,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    @property
    def preprocess_handler(self) -> typing.Callable:
        return self._preprocess

    @preprocess_handler.setter
    def preprocess_handler(self, handler: typing.Callable) -> None:
        self._preprocess = handler

    @property
    def segment_handler(self) -> typing.Callable:
        return self._preprocess

    @segment_handler.setter
    def segment_handler(self, handler: typing.Callable) -> None:
        self._segment = handler

    @property
    def embed_handler(self) -> typing.Callable:
        return self._embed

    @embed_handler.setter
    def embed_handler(self, handler: typing.Callable) -> None:
        self._embed = handler

    def save(self) -> None:
        with open('data.json', 'w') as f:
            json.dump(self._data, f, indent=4)
