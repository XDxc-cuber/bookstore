from sqlalchemy import create_engine  #, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine, Text, LargeBinary, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker
import re, jieba
import jieba.analyse


engine = create_engine("postgresql://15418:6@localhost:5432/postgres")

Base = declarative_base()
DBSession = sessionmaker(bind=engine)


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
    

def insert_SearchByTitle():
    print("\nStart insert SearchByTitle...")
    session = DBSession()
    result = session.query(
        Book.id,
        Book.title
    ).all()
    session.close()

    words_bookid = {}
    for bk in result:
        book_id, title = bk
        # 去掉条条框框
        title = re.sub(r'[\(\[\{（【][^)）】]*[\)\]\{\】\）]\s?', '', title)
        title = re.sub(r'[^\w\s]', '', title)
        if title == "":
            continue
        # 使用搜索模式分词，粒度更细
        words_list = jieba.cut_for_search(title)
        # 建立 分词 -> [书本] 的映射，便于设置rank，从而方便后续的分页
        for word in words_list:
            if word in words_bookid:
                words_bookid[word].append(book_id)
            else:
                words_bookid[word] = [book_id]

    session = DBSession()
    for word, book_ids in words_bookid.items():
        rank = 0
        for book_id in book_ids:
            new_row = SearchByTitle(
                title = word,
                rank = rank,
                book_id = book_id
            )
            session.add(new_row)
            rank += 1
    session.commit()
    session.close()
    del result, words_bookid
        

def insert_SearchByTags():
    print("\nStart insert SearchByTags...")
    session = DBSession()
    result = session.query(
        Book.id,
        Book.tags
    ).all()
    session.close()

    # tags本身相当于分好词了，不需要分词处理
    words_bookid = {}
    for bk in result:
        book_id, tags = bk
        tag_list = tags.strip().split('\n')
        for tag in tag_list:
            tag = tag.strip()
            if tag in words_bookid:
                words_bookid[tag].append(book_id)
            else:
                words_bookid[tag] = [book_id]
    
    session = DBSession()
    for word, book_ids in words_bookid.items():
        rank = 0
        for book_id in book_ids:
            new_row = SearchByTag(
                tag = word,
                rank = rank,
                book_id = book_id
            )
            session.add(new_row)
            rank += 1
    session.commit()
    session.close()
    del result, words_bookid


def insert_SearchByAuthor():
    print("\nStart insert SearchByAuthor...")
    session = DBSession()
    result = session.query(
        Book.id,
        Book.author
    ).all()
    session.close()

    # 拆分出姓名的所有前后缀，作为分词结果
    words_bookid = {}
    for bk in result:
        book_id, author = bk
        if author is None or author == 'None':
            continue
        # 提取国家信息
        res = re.findall(r'[(\[（](.*?)[)\]）]', author)
        if len(res) != 0:
            if res[0] in words_bookid:
                words_bookid[res[0]].append(book_id)
            else:
                words_bookid[res[0]] = [book_id]

        # 放入名字前后缀
        author = re.sub(r'[(\[（](.*?)[)\]）]', "", author).strip()
        author = re.sub(r'[ ·・]', "", author)
        l = len(author)
        for i in range(1, l):
            word = author[:i]
            if word in words_bookid:
                words_bookid[word].append(book_id)
            else:
                words_bookid[word] = [book_id]
            word = author[l-i:]
            if word in words_bookid:
                words_bookid[word].append(book_id)
            else:
                words_bookid[word] = [book_id]
        # 放入名字本身
        if author in words_bookid:
            words_bookid[author].append(book_id)
        else:
            words_bookid[author] = [book_id]

    session = DBSession()
    for word, book_ids in words_bookid.items():
        rank = 0
        for book_id in book_ids:
            new_row = SearchByAuthor(
                author = word,
                rank = rank,
                book_id = book_id
            )
            session.add(new_row)
            rank += 1
    session.commit()
    session.close()
    del result, words_bookid


def insert_SearchByBookIntro():
    print("\nStart insert SearchByBookIntro...")
    session = DBSession()
    result = session.query(
        Book.id,
        Book.book_intro
    ).all()
    session.close()
    
    # 使用TextRank算法提取每本书的介绍中的关键词，作为书本介绍的分词结果
    words_bookid = {}
    tr = jieba.analyse.TextRank()
    for bk in result:
        book_id, book_intro = bk
        key_words = tr.textrank(book_intro, topK=3)
        for word in key_words:
            if word in words_bookid:
                words_bookid[word].append(book_id)
            else:
                words_bookid[word] = [book_id]

    session = DBSession()
    for word, book_ids in words_bookid.items():
        rank = 0
        for book_id in book_ids:
            new_row = SearchByBookIntro(
                book_intro = word,
                rank = rank,
                book_id = book_id
            )
            session.add(new_row)
            rank += 1
    session.commit()
    session.close()
    del result, words_bookid


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    
    # insert
    insert_SearchByTitle()
    insert_SearchByTags()
    insert_SearchByAuthor()
    insert_SearchByBookIntro()

    print("Done")
