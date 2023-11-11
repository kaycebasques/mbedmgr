import threading
import uuid
import json
import fnmatch

import requests

from .base_source import BaseSource

class GithubSource(BaseSource):

    def __init__(self, mbedmgr, owner, repo, tree, include, exclude):
        super().__init__(mbedmgr)
        self._owner = owner
        self._repo = repo
        self._tree = tree
        self._include = include
        self._exclude = exclude
        self._find()

    def get_tree_url(self, path=None):
        return f'https://api.github.com/repos/{self._owner}/{self._repo}/git/trees/{self._tree}?recursive=1'

    def get_path_url(self, path):
        return f'https://raw.githubusercontent.com/{self._owner}/{self._repo}/{self._tree}/{path}'

    def _find(self):
        url = self.get_tree_url()
        response = requests.get(url)
        data = json.loads(response.text)
        for file in data['tree']:
            include = False
            exclude = False
            path = file['path']
            for pattern in self._include:
                if fnmatch.fnmatch(path, pattern):
                    include = True
            for pattern in self._exclude:
                if fnmatch.fnmatch(path, pattern):
                    exclude = True
            if include and not exclude:
                path_url = self.get_path_url(path)
                self.set_text(path_url, None)

    def _scrape(self, mgr, url):
        unused = mgr
        response = requests.get(url)
        if not response.ok:
            return
        self.set_text(url, str(response.text))
