import uuid
import logging
from be.model import error

import datetime
from be.model.db import DB
from be.model.db import User, Book, StoreBook, StoreUser, Order, OrderBook

class myBuyer(DB):
    def __init__(self):
        DB.__init__(self)

    def new_order(self, user_id: str, store_id: str, id_and_count: list[(str, int)]) -> tuple((int, str, str)):
        order_id = ""
        session = None
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id, )
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id, )
            order_id = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))
            
            new_order = Order(
                    order_id = order_id,
                    time = datetime.datetime.now(),
                    total_price = 0,
                    status = 0,
                    fk_buyer_id = user_id,
                    fk_store_id = store_id,
                )
            details = []
            session = self.DbSession()
            for book_id, count in id_and_count:
                result = session.query(
                    Book.price,
                    StoreBook
                    ).join(
                        StoreBook,
                        Book.id == StoreBook.fk_book_id
                    ).filter(
                        Book.id == book_id,
                        StoreBook.fk_store_id == store_id
                    ).first()
                if result is None:
                    session.close()
                    return error.error_non_exist_book_id(book_id) + (order_id, )

                stock_level = result[1].stock_level
                price = result[0]

                if stock_level < count:
                    session.close()
                    return error.error_stock_level_low(book_id) + (order_id,)

                result[1].stock_level -= count
                session.add(result[1])
                new_order.total_price += price * count
                details.append((count, price, book_id))
                
            session.add(new_order)

            for d in details:
                o_b = OrderBook(
                    num = d[0],
                    price = d[1],
                    fk_book_id = d[2],
                    fk_order_id = order_id
                )
                session.add(o_b)
                
            # 所有事务结束后，提交
            session.commit()
            session.close()
            del details
        
        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e)), ""
        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> tuple((int, str)):
        session = None
        try:
            session = self.DbSession()
            order = session.query(
                    Order
                ).filter(
                    Order.order_id == order_id
                ).first()

            if order is None:
                session.close()
                return error.error_invalid_order_id(order_id)

            buyer_id = order.fk_buyer_id
            store_id = order.fk_store_id
            total_price = order.total_price

            if buyer_id != user_id:
                session.close()
                return error.error_authorization_fail()

            buyer = session.query(
                    User
                ).filter(
                    User.user_id == buyer_id
                ).first()
            if buyer is None:
                session.close()
                return error.error_non_exist_user_id(buyer_id)

            balance = buyer.balance
            if password != buyer.password:
                session.close()
                return error.error_authorization_fail()

            seller_id = session.query(
                    StoreUser.fk_user_id
                ).filter(
                    StoreUser.fk_store_id == store_id
                ).first()
            seller_id = seller_id[0]

            if seller_id is None:
                session.close()
                return error.error_non_exist_store_id(store_id)
            if balance < total_price:
                session.close()
                return error.error_not_sufficient_funds(order_id)

            seller = session.query(
                    User
                ).filter(
                    User.user_id == seller_id
                ).first()

            cur_time = datetime.datetime.now()
            cur_time = datetime.date(cur_time.year, cur_time.month, cur_time.day)
            if (cur_time - order.time).days > 3:
                # 支付超时(3天)
                order.status = -1
                session.add(order)
                try:
                    session.commit()
                    session.close()
                    return error.error_order_timed_out(order_id)
                except BaseException as e:
                    session.rollback()
                    logging.info("530, {}".format(str(e)))
                    return 530, "{}".format(str(e))

            buyer.balance -= total_price
            seller.balance += total_price
            order.status = 1
            session.add(buyer)
            session.add(seller)
            session.add(order)
            session.commit()
            session.close()

        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> tuple((int, str)):
        session = None
        try:
            session = self.DbSession()
            user = session.query(
                    User
                ).filter(
                    User.user_id == user_id
                ).first()
                
            if user is None:
                session.close()
                return error.error_authorization_fail()
            if user.password != password:
                session.close()
                return error.error_authorization_fail()

            user.balance += add_value
            session.add(user)
            session.commit()
            session.close()
            
        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e)), ""
        return 200, "ok"

    def search_orders(self, user_id, password) -> tuple((int, str, [])):
        session = None
        try:
            cur_time = datetime.datetime.now()
            cur_time = datetime.date(cur_time.year, cur_time.month, cur_time.day)

            session = self.DbSession()
            user = session.query(
                    User
                ).filter(
                    User.user_id == user_id
                ).first()
            if user is None:
                session.close()
                return error.error_authorization_fail()
            if user.password != password:
                session.close()
                return error.error_authorization_fail()

            orders = []
            result = session.query(
                    Order
                ).filter(
                    Order.fk_buyer_id == user_id
                ).all()
            for od in result:
                # 支付超时
                if (cur_time - od.time).days > 3:
                    od.status = -1
                    session.add(od)
                    continue
                order = {
                    "order_id": od.order_id,
                    "time": od.time,
                    "total_price": od.total_price,
                    "status": od.status
                }
                orders.append(order)

            session.commit()
            session.close()

        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e)), []
        return 200, "ok", orders

    def cancel_order(self, order_id, user_id, password) -> tuple((int, str)):
        session = None
        try:
            session = self.DbSession()
            user = session.query(
                    User
                ).filter(
                    User.user_id == user_id
                ).first()
            if user is None:
                session.close()
                return error.error_authorization_fail()
            if user.password != password:
                session.close()
                return error.error_authorization_fail()

            order = session.query(
                Order
            ).filter(
                Order.order_id == order_id,
                Order.fk_buyer_id == user_id
            ).first()
            if order is None:
                session.close()
                return error.error_change_others_order(user_id, order_id)
            if order.status != 0:
                session.close()
                return error.error_order_status_not_fit(order_id)

            order.status = -1
            session.add(order)
            session.commit()
            session.close()

        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"

    def take_delivery(self, order_id, user_id, password) -> tuple((int, str)):
        session = None
        try:
            session = self.DbSession()
            user = session.query(
                    User
                ).filter(
                    User.user_id == user_id
                ).first()
            if user is None:
                session.close()
                return error.error_authorization_fail()
            if user.password != password:
                session.close()
                return error.error_authorization_fail()

            order = session.query(
                Order
            ).filter(
                Order.order_id == order_id,
                Order.fk_buyer_id == user_id
            ).first()
            if order is None:
                session.close()
                return error.error_change_others_order(user_id, order_id)
            if order.status != 2:
                session.close()
                return error.error_order_status_not_fit(order_id)

            order.status = 3
            session.add(order)
            session.commit()
            session.close()

        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"