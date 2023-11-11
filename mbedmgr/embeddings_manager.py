import sys

from .website_source import WebsiteSource
from .github_source import GithubSource

class EmbeddingsManager:
    def __init__(self, checksums=None):
        self._sources = {}
        self._checksums = checksums

    def get_checksums(self):
        return self._checksums

    def add_website_source(self, source_id, urls=None):
        mbedmgr = self
        website_source = WebsiteSource(mbedmgr, urls)
        self._sources[source_id] = website_source
        return website_source

    def add_github_source(self, source_id, owner, repo, tree, include, exclude):
        mbedmgr = self
        github_source = GithubSource(mbedmgr, owner, repo, tree, include, exclude)
        self._sources[source_id] = github_source
        return github_source

    def generate(self):
        for source_id in self._sources:
            source = self._sources[source_id]
            source.scrape()
            source.preprocess()
            source.segment()
            source.embed()
