from .sitemap_scraper import SitemapScraper

class EmbeddingsManager:
    def __init__(self):
        print('Hello, EmbeddingsManager!')
    def scrape_sitemap(self, sitemap_url):
        scraper = SitemapScraper(sitemap_url)
        urls = scraper.scrape()
        return urls
