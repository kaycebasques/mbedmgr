import sys

from .website_source import WebsiteSource

class EmbeddingsManager:
    def __init__(self):
        self._website_sources = {}

    def add_website_source(self, source_id: str = None) -> WebsiteSource:
        website_source = WebsiteSource()
        self._website_sources[source_id] = website_source
        return website_source

        # self._sitemaps = []
    # def add_sitemap(self, url):
    #     self._sitemaps.append(url)
    # def generate_embeddings(self):
    #     pass
    # def scrape_sitemap(self, sitemap_url):
    #     scraper = SitemapScraper(sitemap_url)
    #     urls = scraper.scrape()
    #     return urls
    # def scrape_urls(self, urls):
    #     scraper = UrlScraper()
    #     scraper.scrape_urls(urls)
    #     return scraper.data
