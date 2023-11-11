import threading
import json

import requests
import bs4
import lxml

from .base_source import BaseSource

class WebsiteSource(BaseSource):

    def __init__(self, mbedmgr, urls=None):
        super().__init__(mbedmgr)
        if urls:
            for url in urls:
                self.set_text(url, None)

    def scrape_urls_from_sitemap(self, sitemap):
        self._sitemap = sitemap
        response = requests.get(sitemap)
        root = lxml.etree.fromstring(response.content)
        namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.xpath('//sitemap:loc', namespaces=namespaces)]
        for url in urls:
            self.set_text(url, None)
