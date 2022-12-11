import sqlite3 as sqlite
from be.model import error
from be.model.db import DB
from be.model.db import StoreBook, Store, StoreUser, Order


class mySeller(DB):
    
    def __init__(self):
        DB.__init__(self)
    
    def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int):
        session = None
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            storebook = StoreBook(
                stock_level=stock_level, 
                book_info = book_json_str, 
                fk_store_id=store_id, 
                fk_book_id=book_id
            )
            session = self.DbSession()
            session.add(storebook)
            session.commit()
            session.close()
            
        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"
    
    def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
        session = None
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            session = self.DbSession()
            result = session.query(
                StoreBook
            ).filter(
                StoreBook.fk_store_id==store_id, StoreBook.fk_book_id==book_id
            ).first()
            
            if result:
                result.stock_level += add_stock_level
                session.add(result)
                session.commit()
            session.close()
            
        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> tuple((int, str)):
        session = None
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            session = self.DbSession()
            newStore = Store(store_id=store_id)
            newStoreUser = StoreUser(fk_store_id=store_id, fk_user_id=user_id)
            session.add(newStore)
            session.add(newStoreUser)
            session.commit()
            session.close()
            
        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"
    
    def deliver_goods(self, order_id, store_id) -> tuple((int ,str)):
        session = None
        try:
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            
            session = self.DbSession()
            order = session.query(
                Order
            ).filter(
                Order.order_id == order_id,
                Order.fk_store_id == store_id
            ).first()
            if order is None:
                session.close()
                return error.error_change_other_store_order(store_id, order_id)
            if order.status != 1:
                session.close()
                return error.error_order_status_not_fit(order_id)

            order.status = 2
            session.add(order)
            session.commit()
            session.close()

        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"