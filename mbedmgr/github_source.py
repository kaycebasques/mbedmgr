import threading
import uuid
import json
import fnmatch

import requests

class GithubSource:

    def __init__(self, owner, repo, tree):
        self._owner = owner
        self._repo = repo
        self._tree = tree
        self._ignore = []
        self._include = []
        self._paths = []
        self._data = {}

    @property
    def include(self):
        return self._include

    @include.setter
    def include(self, patterns):
        self._include = patterns

    @property
    def ignore(self):
        return self._ignore

    @ignore.setter
    def ignore(self, patterns):
        self._ignore = patterns

    def find(self):
        url = f'https://api.github.com/repos/{self._owner}/{self._repo}/git/trees/{self._tree}?recursive=1'
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

    def scrape(self):
        threads = []
        for path in self._paths:
            thread = threading.Thread(target=self._scrape, name=path, args=(path,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        print(self._data)

    def _scrape(self, path):
        url = f'https://raw.githubusercontent.com/{self._owner}/{self._repo}/{self._tree}/{path}'
        response = requests.get(url)
        if not response.ok:
            return
        self._data[path] = str(response.text)

    # @property
    # def embed_handler(self) -> typing.Callable:
    #     return self._embed

    # @embed_handler.setter
    # def embed_handler(self, handler: typing.Callable) -> None:
    #     self._embed = handler
