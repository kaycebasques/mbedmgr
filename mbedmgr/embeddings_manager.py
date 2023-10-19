from .sitemap_scraper import SitemapScraper
from .html_scraper import HtmlScraper

class EmbeddingsManager:
    def __init__(self):
        print('Hello, EmbeddingsManager!')
    def scrape_sitemap(self, sitemap_url):
        scraper = SitemapScraper(sitemap_url)
        urls = scraper.scrape()
        return urls
    def scrape_urls(self, urls):
        scraper = HtmlScraper()
        scraper.scrape_urls(urls)
