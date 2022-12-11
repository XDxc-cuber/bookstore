import pytest

from fe.access.buyer import Buyer
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid


class TestSearchOrders:
    seller_id: str
    store_id: str
    buyer_id: str
    password:str
    buy_book_info_list1: [Book]
    buy_book_info_list2: [Book]
    order1_id: str
    order2_id: str
    buyer: Buyer

    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_search_orders_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_search_orders_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_search_orders_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id

        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list1 = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list1 = gen_book.buy_book_info_list
        assert ok
        ok, buy_book_id_list2 = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list2 = gen_book.buy_book_info_list
        assert ok

        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order1_id = b.new_order(self.store_id, buy_book_id_list1)
        assert code == 200
        code, self.order2_id = b.new_order(self.store_id, buy_book_id_list2)
        assert code == 200
        yield

    def test_ok(self):
        code = self.buyer.search_orders()
        assert code == 200

    def test_authorization_error(self):
        self.buyer.password = self.buyer.password + "_x"
        code = self.buyer.search_orders()
        assert code != 200

