import threading
import uuid
import json
import fnmatch

import requests

class GithubSource:

    def __init__(self, mbedmgr, owner, repo, tree):
        self._mbedmgr = mbedmgr
        self._owner = owner
        self._repo = repo
        self._tree = tree
        self._ignore = []
        self._include = []
        self._paths = []
        self._data = {}
        self._embed = None

    def include(self, patterns):
        self._include = patterns

    def exclude(self, patterns):
        self._ignore = patterns

    def get_tree_url(self, path=None):
        return f'https://api.github.com/repos/{self._owner}/{self._repo}/git/trees/{self._tree}?recursive=1'

    def find(self):
        url = self.get_tree_url()
        response = requests.get(url)
        data = json.loads(response.text)
        for file in data['tree']:
            ignore = False
            include = False
            path = file['path']
            for pattern in self._include:
                if fnmatch.fnmatch(path, pattern):
                    include = True
            for pattern in self._ignore:
                if fnmatch.fnmatch(path, pattern):
                    ignore = True
            if include and not ignore:
                self._paths.append(path)

    # TODO: This is the same logic as website_source.set_page_text() but
    # just different names. So maybe we can inherit a base class?
    def set_text(self, path, text):
        self._data[path] = text

    def get_text(self, path):
        return self._pages[path]

    def get_paths(self):
        paths = []
        for path in self._data:
            paths.append(path)
        return paths

    def scrape(self):
        threads = []
        for path in self._paths:
            thread = threading.Thread(target=self._scrape, name=path, args=(path,self,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def get_path_url(self, path):
        return f'https://raw.githubusercontent.com/{self._owner}/{self._repo}/{self._tree}/{path}'

    def _scrape(self, path, mgr):
        unused = mgr
        url = self.get_path_url(path)
        response = requests.get(url)
        if not response.ok:
            return
        self.set_data(path, str(response.text))

    def embed(self):
        threads = []
        for path in self._data:
            checksums = self._mbedmgr.get_checksums()
            url = self.get_path_url()
            content = self.get_text(path)
            thread = threading.Thread(target=self._embed, name=path, args=(url, text, checksums))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def set_embed_handler(self, handler):
        self._embed = handler
