import requests
import bs4
import threading
import lxml
import typing
import uuid

class WebsiteSource:
    def __init__(self):
        self._urls = {}

    @property
    def urls(self) -> typing.List[str]:
        return self._urls

    @urls.setter
    def urls(self, urls: typing.List[str]) -> None:
        self._urls = urls

    def scrape_sitemap(self, sitemap_url: str) -> None:
        response = requests.get(sitemap_url)
        root = lxml.etree.fromstring(response.content)
        namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.xpath('//sitemap:loc', namespaces=namespaces)]
        for url in urls:
            self._urls[url] = {}

    def _scrape(self, url: str) -> None:
        response = requests.get(url)
        if not response.ok:
            return
        self._urls[url] = {
            'text': response.text,
            'type': response.headers.get('Content-Type')
        }

    def scrape_urls(self) -> None:
        threads = []
        for index, url in enumerate(self._urls):
            thread_id = str(uuid.uuid4())
            thread = threading.Thread(target=self._scrape, name=thread_id, args=(url,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
