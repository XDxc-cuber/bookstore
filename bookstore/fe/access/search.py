import requests
from urllib.parse import urljoin


class Search:
    def __init__(self, url_prefix):
        self.url_prefix = urljoin(url_prefix, "search/")

    def search_multiple(self, args):
        url = urljoin(self.url_prefix, "multiple")
        r = requests.post(url, json=args)
        return r.status_code, r.json().get("book_result")

    def search_by_title(self, title, page):
        url = urljoin(self.url_prefix, "title")
        json = {"title": title, "page": page}
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("book_result")

    def search_by_tag(self, tag, page):
        url = urljoin(self.url_prefix, "tag")
        json = {"tag": tag, "page": page}
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("book_result")

    def search_by_author(self, author, page):
        url = urljoin(self.url_prefix, "author")
        json = {"author": author, "page": page}
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("book_result")

    def search_by_book_intro(self, book_intro, page):
        url = urljoin(self.url_prefix, "book_intro")
        json = {"book_intro": book_intro, "page": page}
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("book_result")

    def search_by_title_store(self, title, store_id, page):
        url = urljoin(self.url_prefix, "title_store")
        json = {"title": title, "store_id": store_id, "page": page}
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("book_result")

    def search_by_tag_store(self, tag, store_id, page):
        url = urljoin(self.url_prefix, "tag_store")
        json = {"tag": tag, "store_id": store_id, "page": page}
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("book_result")

    def search_by_author_store(self, author, store_id, page):
        url = urljoin(self.url_prefix, "author_store")
        json = {"author": author, "store_id": store_id, "page": page}
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("book_result")

    def search_by_book_intro_store(self, book_intro, store_id, page):
        url = urljoin(self.url_prefix, "book_intro_store")
        json = {"book_intro": book_intro, "store_id": store_id, "page": page}
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("book_result")