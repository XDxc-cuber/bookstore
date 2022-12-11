import jwt
import time
import logging
from be.model import error
from be.model.db import DB, User


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.encode("utf-8").decode("utf-8")


def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


class myUser(DB):
    
    def __init__(self):
        DB.__init__(self)
        self.token_lifetime: int = 3600
        
    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False
        
    def register(self, user_id: str, password: str):
        session = None
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            
            newUser = User(
                user_id = user_id,
                password = password,
                balance = 0,
                token = token,
                terminal = terminal,
            )

            session = self.DbSession()
            session.add(newUser)
            session.commit()
            session.close()
            
        except:
            session.rollback()
            return error.error_exist_user_id(user_id)
        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> tuple((int, str)):
        session = self.DbSession()
        result = session.query(
            User.token
        ).filter(
            User.user_id == user_id
        ).first()
        session.close()
        
        if result is None:
            return error.error_authorization_fail()
        db_token = result[0]
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> tuple((int, str)):
        session = self.DbSession()
        result = session.query(
            User.password
        ).filter(
            User.user_id == user_id
        ).first()
        session.close()
        if result is None:
            return error.error_authorization_fail()
        if password != result[0]:
            return error.error_authorization_fail()

        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> tuple((int, str, str)):
        session = None
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            session = self.DbSession()
            user = session.query(
                User
            ).filter(
                User.user_id == user_id
            ).first()
            if user is None:
                session.close()
                return error.error_authorization_fail()
            
            user.token = token
            session.add(user)
            session.commit()
            session.close()
            
        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e)), ""
        return 200, "ok", token

    def logout(self, user_id: str, token: str) -> bool:
        session = None
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)

            session = self.DbSession()
            user = session.query(
                User
            ).filter(
                User.user_id == user_id
            ).first()
            if user is None:
                session.close()
                return error.error_authorization_fail()
            
            user.terminal = terminal
            user.token = dummy_token
            session.add(user)
            session.commit()
            session.close()
            
        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"

    def unregister(self, user_id: str, password: str) -> tuple((int, str)):
        session = None
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            session = self.DbSession()
            session.query(User).filter(User.user_id == user_id).delete()
            session.commit()
            session.close()
            
        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"

    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        session = None
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            
            session = self.DbSession()
            user = session.query(User).filter(User.user_id == user_id).first()
            if user is None:
                session.close()
                return error.error_authorization_fail()
            
            user.password = new_password
            user.terminal = terminal
            user.token = token
            session.add(user)
            session.commit()
            session.close()

        except BaseException as e:
            session.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"
