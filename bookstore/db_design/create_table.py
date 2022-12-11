from sqlalchemy import Column, String, create_engine, Integer, Text, Date, LargeBinary, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker,scoped_session,relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


engine = create_engine("postgresql://15418:6@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = scoped_session(Session)
DbSession = sessionmaker(bind=engine)
session = DbSession()
Base = declarative_base()


"""应用主要数据表"""

class User(Base):
    """用户表"""
    __tablename__ = "User"
    user_id = Column(String(128), primary_key=True, comment="用户名")
    password = Column(String(128), nullable=False, comment="密码")
    balance = Column(Integer, nullable=False, comment="余额")
    token = Column(Text, nullable=False, comment="token")
    terminal = Column(String(32), nullable=False, comment="terminal")
    
class Store(Base):
    """书店表"""
    __tablename__ = "Store"
    store_id = Column(String(128), primary_key=True, comment="书店id")
    
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
    
class StoreUser(Base):
    """书店-店主 关系表"""
    __tablename__ = "StoreUser"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    fk_store_id = Column(
        String(128),
        ForeignKey(
            "Store.store_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="书店"
    )
    fk_user_id = Column(
        String(128),
        ForeignKey(
            "User.user_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="店主"
    )
    """用于正反查询，店主和书店"""
    owner = relationship(
        "User",
        backref="store_user",
    )
    store = relationship(
        "Store",
        backref="store_user",
    )
    
class StoreBook(Base):
    """书店-书本 关系表"""
    __tablename__ = "StoreBook"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    stock_level = Column(Integer, nullable=False, comment="库存")
    book_info = Column(Text, nullable=False, comment="书本信息")
    fk_store_id = Column(
        String(128),
        ForeignKey(
            "Store.store_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="书店"
    )
    fk_book_id = Column(
        String(8),
        ForeignKey(
            "Book.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="书本"
    )
    
    """用于正反查询，书店和书本"""
    store = relationship(
        "Store",
        backref="store_book",
    )
    book = relationship(
        "Book",
        backref="store_book",
    )
    
class Order(Base):
    """订单表"""
    __tablename__ = "Order"
    order_id = Column(String(200), primary_key=True, comment="主键")
    time = Column(Date, nullable=False, comment="时间")
    total_price = Column(Integer, nullable=False, comment="总价")
    """
        status:
            0: 待付款
            1: 待发货
            2: 已发货
            3: 已收货
           -1: 已取消
    """
    status = Column(Integer, nullable=False, comment="状态")
    
    fk_buyer_id = Column(
        String(128),
        ForeignKey(
            "User.user_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="买方"
    )
    fk_store_id = Column(
        String(128),
        ForeignKey(
            "Store.store_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="书店"
    )
    
class OrderBook(Base):
    """
       订单-书本对应表
       一个订单可能对应多个书本，一个书本也可能对应多个订单
    """
    __tablename__ = "OrderBook"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    num = Column(Integer, nullable=False, comment="数量")
    price = Column(Integer, nullable=False, comment="总价")
    
    fk_order_id = Column(
        String(200),
        ForeignKey(
            "Order.order_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="订单"
    )
    fk_book_id = Column(
        String(8),
        ForeignKey(
            "Book.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="书本"
    )
    
    """用于正反查询，订单和书本"""
    order = relationship(
        "Order",
        backref="order_book",
    )
    book = relationship(
        "Book",
        backref="order_book",
    )



"""搜索用倒排索引表"""

class SearchByTitle(Base):
    """标题搜索表"""
    __tablename__ = 'SearchByTitle'
    title = Column(Text, nullable=False)
    rank = Column(Integer, nullable=False)
    book_id = Column(
        String(8), 
        ForeignKey(
            'Book.id',
            ondelete="CASCADE",
            onupdate="CASCADE",
        ), 
        nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint('title', 'rank'),
        {},
    )

class SearchByTag(Base):
    """标签搜索表"""
    __tablename__ = 'SearchByTag'
    tag = Column(Text, nullable=False)
    rank = Column(Integer, nullable=False)
    book_id = Column(
        String(8), 
        ForeignKey(
            'Book.id',
            ondelete="CASCADE",
            onupdate="CASCADE",
        ), 
        nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint('tag', 'rank'),
        {},
    )

class SearchByAuthor(Base):
    """作者搜索表"""
    __tablename__ = 'SearchByAuthor'
    author = Column(String(32), nullable=False)
    rank = Column(Integer, nullable=False)
    book_id = Column(
        String(8), 
        ForeignKey(
            'Book.id',
            ondelete="CASCADE",
            onupdate="CASCADE",
        ), 
        nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint('author', 'rank'),
        {},
    )

class SearchByBookIntro(Base):
    """书本介绍搜索表"""
    __tablename__ = 'SearchByBookIntro'
    book_intro = Column(Text, nullable=False)
    rank = Column(Integer, nullable=False)
    book_id = Column(
        String(8), 
        ForeignKey(
            'Book.id',
            ondelete="CASCADE",
            onupdate="CASCADE",
        ), 
        nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint('book_intro', 'rank'),
        {},
    )




if __name__ == "__main__":
    # 删除表
    print("Deleting tables...")
    Base.metadata.drop_all(engine)

    # 创建表
    print("Creating tables...")
    Base.metadata.create_all(engine)

    print("Done")
    