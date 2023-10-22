import requests
import bs4
import threading
import lxml
import typing

class WebsiteSource:
    def __init__(self):
        self.urls = None

    @property
    def urls(self) -> typing.List[str]:
        print('Hello from the setter!')
        return self._urls

    @urls.setter
    def urls(self, urls: typing.List[str]) -> None:
        self._urls = urls

    # TODO: Rename? Not sure if should use `scrape` too much...
    def scrape_sitemap(self, sitemap_url: str) -> None:
        response = requests.get(sitemap_url)
        # If you try to use `response.text` here `lxml` throws the following error:
        # `ValueError: Unicode strings with encoding declaration are not supported.`
        root = lxml.etree.fromstring(response.content)
        namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        # TODO: Should be Dict. Will need to add content, metadata, etc.
        self.urls = [loc.text for loc in root.xpath('//sitemap:loc', namespaces=namespaces)]

    def _scrape(self, url):
        response = requests.get(url)
        if not response.ok:
            return
        self._data[url] = {
            'text': response.text,
            'type': response.headers.get('Content-Type')
        }

    def scrape_urls(self):
        threads = []
        for index, url in enumerate(self.urls):
            thread_id = f't{index}'
            thread = threading.Thread(target=self.scrape_url, name=thread_id, args=(url,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()



# 
# class SitemapScraper:
#     def __init__(self, sitemap_url):
#         self._sitemap_url = sitemap_url
#     def scrape(self):
# import requests
# import bs4
# import threading
# import lxml
# 
# class UrlScraper:
#     def __init__(self):
#         self._data = {}
# 
#     def scrape_url(self, url):
#         response = requests.get(url)
#         if not response.ok:
#             return
#         self._data[url] = {
#             'text': response.text,
#             'type': response.headers.get('Content-Type')
#         }
# 
#     def scrape_urls(self, urls):
#         threads = []
#         for index, url in enumerate(urls):
#             thread_id = f't{index}'
#             thread = threading.Thread(target=self.scrape_url, name=thread_id, args=(url,))
#             threads.append(thread)
#             thread.start()
#         for thread in threads:
#             thread.join()
# 
#     @property
#     def data(self):
#         return self._data
