import requests
import bs4
import threading
import lxml

# def scrape_title(url):
#     response = requests.get(url)
#     soup = bs4.BeautifulSoup(response.text, 'html.parser')
#     title = soup.find('title')
#     print(title)
#     # html = soup.get_text()
#     # markdown = mistune.markdown(html)
# 
# threads = []
# response = requests.get('https://pigweed.dev/sitemap.xml')
# sitemap = ElementTree.fromstring(response.text)
# locs =  sitemap.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
# for index, loc in enumerate(locs):
#     url = loc.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
#     if url is None:
#         continue
#     name = f't{index}'
#     thread = threading.Thread(target=scrape_title, name=name, args=(url,))
#     thread.start()
#     threads.append(thread)
# 
# for thread in threads:
#     thread.join()



class SitemapScraper:
    def __init__(self, sitemap_url):
        self._sitemap_url = sitemap_url
    def scrape(self):
        response = requests.get(self._sitemap_url)
        # If you try to use `response.text` here `lxml` throws the following error:
        # `ValueError: Unicode strings with encoding declaration are not supported.`
        root = lxml.etree.fromstring(response.content)
        namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.xpath('//sitemap:loc', namespaces=namespaces)]
        return urls
