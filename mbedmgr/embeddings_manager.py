import sys

from .website_source import WebsiteSource
from .github_source import GithubSource

class EmbeddingsManager:
    def __init__(self):
        self._website_sources = {}
        self._github_sources = {}

    def add_website_source(self, source_id: str = None) -> WebsiteSource:
        website_source = WebsiteSource()
        self._website_sources[source_id] = website_source
        return website_source

    def add_github_source(self, owner, repo, tree) -> GithubSource:
        github_source = GithubSource(owner, repo, tree)
        source_id = f'{owner}_{repo}_{tree}'
        self._github_sources[source_id] = github_source
        return github_source

    def generate(self) -> None:
        for source_id in self._website_sources:
            source = self._website_sources[source_id]
            source.scrape()
            source.preprocess()
            source.segment()
            source.embed()
        for source_id in self._github_sources:
            source = self._github_sources[source_id]
            source.find()
            source.scrape()
            source.embed()
