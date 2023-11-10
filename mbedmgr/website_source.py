import threading
import json

import requests
import bs4
import lxml

# TODO: Get the API naming consistent. E.g. set_pages versus page_handler (no verb in the setter)

class WebsiteSource:

    def __init__(self):
        self._pages = {}
        self._scrape = self._default_scrape_handler
        self._preprocess = self._default_preprocess_handler
        self._segment = False
        self._embed = False
        self._sitemap = None

    @property
    def sitemap(self):
        return self._sitemap

    @sitemap.setter
    def sitemap(self, sitemap_url):
        self._sitemap = sitemap_url
        response = requests.get(sitemap_url)
        root = lxml.etree.fromstring(response.content)
        namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.xpath('//sitemap:loc', namespaces=namespaces)]
        for url in urls:
            self._pages[url] = {}

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, urls):
        for url in urls:
            self._pages[url] = {}

    @property
    def scrape_handler(self):
        return self._scrape

    @scrape_handler.setter
    def scrape_handler(self, handler):
        self._scrape = handler

    def _default_scrape_handler(self, url, mgr):
        response = requests.get(url)
        if not response.ok:
            return
        mgr.set_page_text(url, response.text)

    def scrape(self):
        threads = []
        for url in self._pages:
            data = self._pages[url]
            # TODO it's ok to pass mgr here, the buganizer was a trap
            thread = threading.Thread(target=self._scrape, name=url, args=(url,data,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def get_page_text(self, url):
        return self._pages[url]['text']
    
    def set_page_text(self, url, text):
        self._pages[url]['text'] = text
    
    @property
    def preprocess_handler(self):
        return self._preprocess

    @preprocess_handler.setter
    def preprocess_handler(self, handler):
        self._preprocess = handler

    def _default_preprocess_handler(self, url, mgr):
        text = self.get_page_text(url)
        soup = bs4.BeautifulSoup(text, 'html.parser')
        body = soup.find('body')
        for tag_name in ['script', 'style', 'link']:
            for useless_tag in body.find_all(tag_name):
                useless_tag.decompose()
        mgr.set_page_text(url, str(body))

    def preprocess(self):
        if self._preprocess is False:
            return
        threads = []
        for url in self._pages:
            data = self._pages[url]
            # TODO it's ok to pass mgr here, the buganizer was a trap
            thread = threading.Thread(target=self._preprocess, name=url, args=(url,data,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    @property
    def segment_handler(self):
        return self._preprocess

    @segment_handler.setter
    def segment_handler(self, handler):
        self._segment = handler

    def segment(self):
        if self._segment is False:
            return
        threads = []
        for url in self._pages:
            # TODO: It's not necessary to give them access to the whole data object.
            thread = threading.Thread(target=self._segment, name=url, args=(url,self,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    @property
    def embed_handler(self):
        return self._embed

    @embed_handler.setter
    def embed_handler(self, handler):
        self._embed = handler

    def embed(self):
        if self._embed is False:
            return
        threads = []
        for url in self._pages:
            # TODO: It's not necessary to give them access to the whole data object.
            thread = threading.Thread(target=self._embed, name=url, args=(url,self,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
