from .sitemap_scraper import SitemapScraper
from .url_scraper import UrlScraper

class EmbeddingsManager:
    def __init__(self):
        print('Hello, EmbeddingsManager!')
    def scrape_sitemap(self, sitemap_url):
        scraper = SitemapScraper(sitemap_url)
        urls = scraper.scrape()
        return urls
    def scrape_urls(self, urls):
        scraper = UrlScraper()
        scraper.scrape_urls(urls)
        return scraper.data
