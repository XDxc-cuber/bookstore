from be.model.db import DB, Book, StoreBook
from sqlalchemy import and_

class mySearch(DB):
    def __init__(self):
        DB.__init__(self)

    def get_search_key(self, key):
        if not key or not type(key) is str:
            return key
        if key == "":
            return None
        return '%' + key + '%'

    def search_by_title(self, title: str, page: int) -> tuple((int, str, list)):
        ret = []
        try:
            session = self.DbSession()
            result = session.execute(
                "SELECT id, title, author, tags, book_intro \
                FROM \"Book\" WHERE id in \
                (SELECT book_id FROM \"SearchByTitle\" WHERE title='%s' AND rank BETWEEN %d and %d)"
                % (title, (page-1)*10, page*10-1)).fetchall()
            ret = [{
                    "book id": bk[0],
                    "title": bk[1],
                    "author": bk[2],
                    "tags": bk[3],
                    "book intro": bk[4]
                    } for bk in result]

        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", ret

    def search_by_tag(self, tag: str, page: int) -> tuple((int, str, list)):
        ret = []
        try:
            session = self.DbSession()
            result = session.execute(
                "SELECT id, title, author, tags, book_intro \
                FROM \"Book\" WHERE id in \
                (SELECT book_id FROM \"SearchByTag\" WHERE tag='%s' AND rank BETWEEN %d and %d)"
                % (tag, (page-1)*10, page*10-1)).fetchall()
            ret = [{
                    "book id": bk[0],
                    "title": bk[1],
                    "author": bk[2],
                    "tags": bk[3],
                    "book intro": bk[4]
                    } for bk in result]

        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", ret

    def search_by_author(self, author: str, page: int) -> tuple((int, str, list)):
        ret = []
        try:
            session = self.DbSession()
            result = session.execute(
                "SELECT id, title, author, tags, book_intro \
                FROM \"Book\" WHERE id in \
                (SELECT book_id FROM \"SearchByAuthor\" WHERE author='%s' AND rank BETWEEN %d and %d)"
                % (author, (page-1)*10, page*10-1)).fetchall()
            ret = [{
                    "book id": bk[0],
                    "title": bk[1],
                    "author": bk[2],
                    "tags": bk[3],
                    "book intro": bk[4]
                    } for bk in result]

        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", ret

    def search_by_book_intro(self, book_intro: str, page: int) -> tuple((int, str, list)):
        ret = []
        try:
            session = self.DbSession()
            result = session.execute(
                "SELECT id, title, author, tags, book_intro \
                FROM \"Book\" WHERE id in \
                (SELECT book_id FROM \"SearchByBookIntro\" WHERE book_intro='%s' AND rank BETWEEN %d and %d)"
                % (book_intro, (page-1)*10, page*10-1)).fetchall()
            ret = [{
                    "book id": bk[0],
                    "title": bk[1],
                    "author": bk[2],
                    "tags": bk[3],
                    "book intro": bk[4]
                    } for bk in result]

        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", ret

    def search_by_title_store(self, title: str, store_id: str, page: int) -> tuple((int, str, list)):
        ret = []
        try:
            session = self.DbSession()
            result = session.execute(
                "SELECT id, title, author, tags, book_intro \
                FROM \"Book\" \
                WHERE id IN \
                (SELECT book_id FROM \"SearchByTitle\" WHERE title='%s') \
                AND id IN \
                (SELECT fk_book_id FROM \"StoreBook\" WHERE fk_store_id='%s') \
                LIMIT 10 OFFSET %d"
                % (title, store_id, (page-1)*10)).fetchall()
            ret = [{
                    "book id": bk[0],
                    "title": bk[1],
                    "author": bk[2],
                    "tags": bk[3],
                    "book intro": bk[4]
                    } for bk in result]

        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", ret

    def search_by_tag_store(self, tag: str, store_id: str, page: int) -> tuple((int, str, list)):
        ret = []
        try:
            session = self.DbSession()
            result = session.execute(
                "SELECT id, title, author, tags, book_intro \
                FROM \"Book\" \
                WHERE id IN \
                (SELECT book_id FROM \"SearchByTag\" WHERE tag='%s') \
                AND id IN \
                (SELECT fk_book_id FROM \"StoreBook\" WHERE fk_store_id='%s') \
                LIMIT 10 OFFSET %d"
                % (tag, store_id, (page-1)*10)).fetchall()
            ret = [{
                    "book id": bk[0],
                    "title": bk[1],
                    "author": bk[2],
                    "tags": bk[3],
                    "book intro": bk[4]
                    } for bk in result]

        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", ret

    def search_by_author_store(self, author: str, store_id: str, page: int) -> tuple((int, str, list)):
        ret = []
        try:
            session = self.DbSession()
            result = session.execute(
                "SELECT id, title, author, tags, book_intro \
                FROM \"Book\" \
                WHERE id IN \
                (SELECT book_id FROM \"SearchByAuthor\" WHERE author='%s') \
                AND id IN \
                (SELECT fk_book_id FROM \"StoreBook\" WHERE fk_store_id='%s') \
                LIMIT 10 OFFSET %d"
                % (author, store_id, (page-1)*10)).fetchall()
            ret = [{
                    "book id": bk[0],
                    "title": bk[1],
                    "author": bk[2],
                    "tags": bk[3],
                    "book intro": bk[4]
                    } for bk in result]

        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", ret

    def search_by_book_intro_store(self, book_intro: str, store_id: str, page: int) -> tuple((int, str, list)):
        ret = []
        try:
            session = self.DbSession()
            result = session.execute(
                "SELECT id, title, author, tags, book_intro \
                FROM \"Book\" \
                WHERE id IN \
                (SELECT book_id FROM \"SearchByBookIntro\" WHERE book_intro='%s') \
                AND id IN \
                (SELECT fk_book_id FROM \"StoreBook\" WHERE fk_store_id='%s') \
                LIMIT 10 OFFSET %d"
                % (book_intro, store_id, (page-1)*10)).fetchall()
            ret = [{
                    "book id": bk[0],
                    "title": bk[1],
                    "author": bk[2],
                    "tags": bk[3],
                    "book intro": bk[4]
                    } for bk in result]

        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", ret

    def search_multiple(self, args: dict) -> tuple((int, str, list)):
        ret = []
        try:
            store_id = self.get_search_key(args.get("store_id"))
            title_key = self.get_search_key(args.get("title_key"))
            author_key = self.get_search_key(args.get("author_key"))
            book_intro_key = self.get_search_key(args.get("book_intro_key"))
            tags_key = self.get_search_key(args.get("tags_key"))
            
            store_filter = (StoreBook.fk_store_id.like(store_id) if store_id else True)
            title_filter = (Book.title.like(title_key) if title_key else True)
            author_filter = (Book.author.like(author_key) if author_key else True)
            book_intro_filter = (Book.book_intro.like(book_intro_key) if book_intro_key else True)
            tags_filter = (Book.tags.like(tags_key) if tags_key else True)
            
            result = []
            session = self.DbSession()
            result = session.query(
                Book.id,
                Book.title,
                Book.author,
                Book.book_intro,
                Book.tags,
                Book.pages,
                StoreBook.fk_store_id,
            ).join(
                StoreBook,
                Book.id == StoreBook.fk_book_id
            ).filter(
                and_(
                    store_filter,
                    title_filter,
                    author_filter,
                    book_intro_filter,
                    tags_filter,
            ))
            session.close()
            
            for bk in result:
                ret.append({
                            'id': bk[0],
                            'title': bk[1], 
                            'author':bk[2], 
                            'book_intro': bk[3],
                            'tags': bk[4],
                            'pages': bk[5],
                            'store id': bk[6]
                            })

        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", ret
    