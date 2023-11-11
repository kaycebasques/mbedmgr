import threading
import json

import requests
import bs4
import lxml

class BaseSource:

    def __init__(self, mbedmgr, checksums=None):
        self._mbedmgr = mbedmgr
        self._data = {}
        self._segments = None
        self._preprocess = None
        self._segment = None
        self._embed = None

    def get_data(self):
        return self._data

    def get_text(self, identifier):
        return self._data[identifier]

    def set_text(self, identifier, text):
        self._data[identifier] = text

    def set_scrape_handler(self, handler):
        self._scrape = handler

    def _scrape(self, mgr, identifier):
        unused = mgr
        response = requests.get(identifier)
        if not response.ok:
            return
        mgr.set_text(identifier, response.text)

    def scrape(self):
        threads = []
        mgr = self
        for identifier in self._data:
            thread = threading.Thread(target=self._scrape, name=identifier, args=(mgr, identifier,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def set_preprocess_handler(self, handler):
        self._preprocess = handler

    def preprocess(self):
        if self._preprocess is None:
            return
        threads = []
        mgr = self
        for identifier in self._data:
            data = self._data[identifier]
            thread = threading.Thread(target=self._preprocess, name=identifier, args=(mgr, identifier,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def get_segments(self):
        return self._segments

    def set_segment(self, identifier, text):
        if self._segments is None:
            self._segments = {}
        self._segments[identifier] = text

    def set_segment_handler(self, handler):
        self._segment = handler

    def segment(self):
        if self._segment is None:
            return
        threads = []
        mgr = self
        for identifier in self._data:
            thread = threading.Thread(target=self._segment, name=identifier, args=(mgr, identifier,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def set_embed_handler(self, handler):
        self._embed = handler

    def embed(self):
        if self._embed is None:
            return
        threads = []
        segments = self.get_segments()
        data = self.get_data() if segments is None else segments
        mgr = self
        for identifier in data:
            checksums = self._mbedmgr.get_checksums()
            text = data[identifier]
            thread = threading.Thread(target=self._embed, name=identifier, args=(mgr, identifier, text, checksums,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
