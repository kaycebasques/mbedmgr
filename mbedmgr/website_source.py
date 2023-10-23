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

    def scrape_pages(self) -> None:
        threads = []
        for url in self._data:
            thread_id = str(uuid.uuid4())
            thread = threading.Thread(target=self._scrape_page, name=thread_id, args=(url,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def minify_pages(self) -> None:
        threads = []
        for url in self._data:
            thread_id = str(uuid.uuid4())
            thread = threading.Thread(target=self._minify_page, name=thread_id, args=(url,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def save(self) -> None:
        with open('data.json', 'w') as f:
            json.dump(self._data, f, indent=4)

    # TODO: Turn this into a caller-defined function.
    def _minify_page(self, url: str) -> None:
        soup = bs4.BeautifulSoup(self._data[url]['text'], 'html.parser')
        main = soup.select('div.main')
        if len(main) != 1:
            print('ERROR: Expected page to have exactly 1 div.main element')
        main = main[0]
        for script in main.find_all('script'):
            script.decompose()
        for style in main.find_all('style'):
            style.decompose()
        for link in main.find_all('link'):
            link.decompose()
        self._data[url]['text'] = str(main)

    def _scrape_page(self, url: str) -> None:
        response = requests.get(url)
        if not response.ok:
            return
        self._data[url] = {
            'text': response.text,
            'type': response.headers.get('Content-Type')
        }
