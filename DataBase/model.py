from sqlalchemy import Column,Integer, BigInteger,ForeignKey,String,SmallInteger,CHAR
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Users (Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement = True, primary_key = True)
    vk_id = Column(BigInteger, unique = True,nullable=False)
    city = Column(Integer)
    age = Column(SmallInteger)
    gender = Column(Integer)
    count = Column(Integer)


class Candidate(Base):
    __tablename__ = 'candidate'

    id = Column(Integer, autoincrement = True, primary_key = True)
    vk_id = Column(BigInteger, unique = True,nullable=False)
    city = Column(Integer)
    age = Column(SmallInteger)
    gender = Column(Integer)


class BlackLists(Base):
    __tablename__ = 'black__lists'

    id = Column(Integer, autoincrement = True, primary_key = True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    candidate_id = Column(Integer,ForeignKey('candidate.id'),nullable=False)

    users = relationship(Users, backref='black__lists')
    candidate = relationship(Candidate, backref='black__lists')

class Likes(Base):
    __tablename__ = 'likes'

    id = Column(Integer, autoincrement = True, primary_key = True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    candidate_id = Column(Integer,ForeignKey('candidate.id'),nullable=False)
    
    users = relationship(Users, backref='likes')
    candidate = relationship(Candidate, backref='likes')

def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables (engine):
    Base.metadata.drop_all(engine)
