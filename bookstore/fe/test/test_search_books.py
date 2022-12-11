import pytest

from fe.access.new_seller import register_new_seller
from fe.access import search, book
from fe import conf
import uuid


class TestLogin:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.search = search.Search(conf.URL)
        self.seller_id = "test_search_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_search_store_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.seller = register_new_seller(self.seller_id, self.password)

        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 5)
        yield

    def test_search_multiple(self):
        args = {"title": "美丽", "store_id": "test_new_order"}
        code, result = self.search.search_multiple(args)
        assert code == 200

        # 检查结果是否符合查询要求
        for bk in result:
            assert "美丽" in bk['title']
            assert "test_new_order" in bk['store id']

    def test_search_by_title(self):
        title = "心灵"
        page = 1
        code, result = self.search.search_by_title(title, page)
        assert code == 200
        for bk in result:
            assert title in bk['title']

    def test_search_by_tag(self):
        tag = "传记"
        page = 1
        code, result = self.search.search_by_tag(tag, page)
        assert code == 200
        for bk in result:
            assert tag in bk['tags']

    def test_search_by_author(self):
        author = "国平"
        page = 1
        code, result = self.search.search_by_author(author, page)
        assert code == 200
        for bk in result:
            assert author in bk['author']

    def test_search_by_book_intro(self):
        book_intro = "再现"
        page = 1
        code, result = self.search.search_by_book_intro(book_intro, page)
        assert code == 200
        for bk in result:
            assert book_intro in bk['book intro']

    def test_search_by_title_store(self):
        title = "心灵"
        store_id = self.store_id
        page = 1
        code, result = self.search.search_by_title_store(title, store_id, page)
        assert code == 200
        for bk in result:
            assert title in bk['title']

    def test_search_by_tag_store(self):
        tag = "漫画"
        store_id = self.store_id
        page = 1
        code, result = self.search.search_by_tag_store(tag, store_id, page)
        assert code == 200
        for bk in result:
            assert tag in bk['tags']

    def test_search_by_author_store(self):
        author = "国平"
        store_id = self.store_id
        page = 1
        code, result = self.search.search_by_author_store(author, store_id, page)
        assert code == 200
        for bk in result:
            assert author in bk['author']

    def test_search_by_book_intro_store(self):
        book_intro = "三毛"
        store_id = self.store_id
        page = 1
        code, result = self.search.search_by_book_intro_store(book_intro, store_id, page)
        assert code == 200
        for bk in result:
            assert book_intro in bk['book intro']
