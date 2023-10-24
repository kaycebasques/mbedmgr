import requests
import bs4
import threading
import lxml
import typing
import uuid
import time
import json

class WebpageData(typing.TypedDict):
    text: str

class WebsiteSource:
    def __init__(self):
        self._data = {}
        self._minify = None

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

    def preprocess(self) -> None:
        if self._preprocess is None:
            print('preprocess() has no effect because a handler was not set.')
            return
        threads = []
        for url in self._data:
            thread_id = str(uuid.uuid4())
            thread = threading.Thread(target=self._preprocess, name=thread_id, args=(url,self._data,))
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

    def save(self) -> None:
        with open('data.json', 'w') as f:
            json.dump(self._data, f, indent=4)

    def _scrape(self, url: str) -> None:
        response = requests.get(url)
        if not response.ok:
            return
        self._data[url] = {
            'text': response.text,
            'type': response.headers.get('Content-Type')
        }
