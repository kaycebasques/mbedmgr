import requests
import bs4
import threading
import lxml

class HtmlScraper:
    def __init__(self):
        self._data = {}
    def _scrape_html(self, url):
        response = requests.get(url)
        self._data[url] = response.text
    def scrape_urls(self, urls):
        threads = []
        for index, url in enumerate(urls):
            thread_id = f't{index}'
            thread = threading.Thread(target=self._scrape_html, name=thread_id, args=(url,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        print(self._data)
