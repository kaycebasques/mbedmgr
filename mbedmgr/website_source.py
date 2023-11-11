import threading
import json

import requests
import bs4
import lxml

class WebsiteSource:

    def __init__(self, mbedmgr):
        self._mbedmgr = mbedmgr
        self._pages = {}
        self._segments = {}
        self._preprocess = None
        self._segment = None
        self._embed = None
        self._sitemap = None

    def set_sitemap(self, sitemap_url):
        self._sitemap = sitemap_url

    def scrape_pages_from_sitemap(self):
        response = requests.get(self._sitemap)
        root = lxml.etree.fromstring(response.content)
        namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.xpath('//sitemap:loc', namespaces=namespaces)]
        for url in urls:
            self._pages[url] = {}

    def get_pages(self):
        return self._pages

    def set_pages(self, urls):
        for url in urls:
            self._pages[url] = {}

    def get_page_text(self, url):
        return self._pages[url]

    def set_page_text(self, url, text):
        self._pages[url] = text

    def set_scrape_handler(self, handler):
        self._scrape = handler

    def _scrape(self, url, mgr):
        unused = mgr
        response = requests.get(url)
        if not response.ok:
            return
        self.set_page_text(url, response.text)

    def scrape(self):
        threads = []
        for url in self._pages:
            thread = threading.Thread(target=self._scrape, name=url, args=(url, self,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def set_preprocess_handler(self, handler):
        self._preprocess = handler

    def preprocess(self):
        if self._preprocess is None:
            return
        threads = []
        for url in self._pages:
            data = self._pages[url]
            thread = threading.Thread(target=self._preprocess, name=url, args=(url, self,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def get_segments(self):
        return self._segments

    def set_segment(self, url, text):
        self._segments[url] = text

    def set_segment_handler(self, handler):
        self._segment = handler

    def segment(self):
        if self._segment is None:
            return
        threads = []
        for url in self._pages:
            thread = threading.Thread(target=self._segment, name=url, args=(url, self,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def set_embed_handler(self, handler):
        self._embed = handler

    def embed(self):
        if self._embed is None:
            return
        threads = []
        segments = self.get_segments()
        for url in segments:
            text = segments[url]
            thread = threading.Thread(target=self._embed, name=url, args=(url, text,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
