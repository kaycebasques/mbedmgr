import requests
import bs4
import threading
import lxml

class UrlScraper:
    def __init__(self):
        self._data = {}

    def scrape_url(self, url):
        response = requests.get(url)
        if not response.ok:
            return
        self._data[url] = {
            'text': response.text,
            'type': response.headers.get('Content-Type')
        }

    def scrape_urls(self, urls):
        threads = []
        for index, url in enumerate(urls):
            thread_id = f't{index}'
            thread = threading.Thread(target=self.scrape_url, name=thread_id, args=(url,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    @property
    def data(self):
        return self._data
