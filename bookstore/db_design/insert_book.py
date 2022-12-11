import sqlite3
from sqlalchemy import create_engine  #, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine, Text, LargeBinary
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://15418:6@localhost:5432/postgres")

Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Book(Base):
    """书籍表"""
    __tablename__ = "Book"
    id = Column(String(8), primary_key=True, comment="主键")
    title = Column(String(32), nullable=False, comment="书名")
    author = Column(String(32), nullable=False, comment="作者")
    publisher = Column(String(32), nullable=False, comment="出版社")
    original_title = Column(Text, nullable=True, comment="原名")
    translator = Column(String(32), nullable=True, comment="译者")
    pub_year = Column(String(8), nullable=False, comment="出版年")
    pages = Column(Integer, nullable=False, comment="页数")
    price = Column(Integer, nullable=False, comment="价格")
    currency_unit = Column(Text, nullable=False, comment="货币单位")
    binding = Column(String(16), nullable=False, comment="装订")
    isbn = Column(String(32), nullable=False, comment="书号")
    author_intro = Column(Text, nullable=False, comment="作者简介")
    book_intro = Column(Text, nullable=False, comment="书本简介")
    content = Column(Text, nullable=False, comment="目录")
    tags = Column(Text, nullable=False, comment="标记")
    picture = Column(LargeBinary, nullable=False, comment="图片")


def init():
    global DBSession, Base
    DBSession = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    
if __name__ == '__main__':
    init()
    
    # insert
    conn = sqlite3.connect(r"D:\onedrive\db\2022_CDMS_PJ2_REQUIRE\bookstore\fe\data\book.db")
    cursor = conn.cursor()
    sql = """select * from book;"""
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    print("Load data from database, Done.")
    
    print("Data size %d" % (len(result)))
    session = DBSession()
    for b in result:
        book = Book(
            id = b[0],
            title = b[1],
            author = b[2],
            publisher = b[3],
            original_title = b[4],
            translator = b[5],
            pub_year = b[6],
            pages = b[7],
            price = b[8],
            currency_unit = b[9],
            binding = b[10],
            isbn = b[11],
            author_intro = b[12],
            book_intro = b[13],
            content = b[14],
            tags = b[15],
            picture = b[16],
        )
        session.add(book)
    del result
    session.commit()
    session.close()
    print("Done")
    
    # check
    session = DBSession()
    result = session.query(Book.title).first()
    session.close()
    print(result)
    

