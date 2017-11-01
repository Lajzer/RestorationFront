import hashlib
from datetime import datetime, timedelta
from settings import *
from sqlalchemy import Column,Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

engine = create_engine('mysql+pymysql://userRF:passRF@localhost/RFront')
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    id_ = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(128))

class BlogPost(Base):
    __tablename__ = 'blogposts'

    id_ = Column(Integer, primary_key=True)
    date = Column(DateTime , default=datetime.utcnow)
    text = Column(String(131072))
    title = Column(String(128))
    author = Column(String(50))
    comment = relationship("Comment")

    def __repr__(self):
        return '<BlogPost: {}>'.format(self.text)

class Comment(Base):
    __tablename__ = 'comments'

    id_ = Column(Integer, primary_key=True)
    date = Column(DateTime , default=datetime.utcnow)
    text = Column(String(65536))
    author = Column(String(50))
    basePost = Column(Integer, ForeignKey('blogposts.id_'))

    def __repr__(self):
        return '<Comment: {}>'.format(self.text)

def get_posts():
    return session.query(BlogPost).all()

def get_post(id__):
    return session.query(BlogPost).filter_by(id_=id__)

def get_post(title_):
    return session.query(BlogPost).filter_by(title=title_)

def new_post(title_, text_, author_="Anonymous"):
    post = BlogPost(text=text_, title=title_,author=author_)
    session.add(post)
    print("huj")
    session.commit()
    return 0

def del_post(id__):
    p = session.query(BlogPost).filter_by(id_=id__).first()
    session.delete(p)
    session.commit()
    return

def update_post(id_, title_, text_):
    return

def new_user(login, passwordHash):
    nu = User(name=login, password=passwordHash)
    session.add(nu)
    session.commit()
    return

def authenticate(name_, passwordHash_):
    uzyt = session.query(User).filter_by(name=name_)
    if uzyt != None and uzyt.password == passwordHash:
        print("zalogowano")
        return 0
    print("zly login lub haslo")
    return 1

def log_in(login, passwordHash):
    session.query(User).filter_by(name=login)
    print("zalogowano")
    return 0


#Base.metadata.create_all(engine)

#print(session.query(User).count())
p = get_posts()
for i in p:
    print(i)
    print(i.title)
    print(i.id_)

