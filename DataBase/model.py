from sqlalchemy import Column,Integer, BigInteger,ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Users (Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement = True, primary_key = True)
    vk_id = Column(BigInteger, unique = True)

class Candidate(Base):
    __tablename__ = 'candidate'

    id = Column(Integer, autoincrement = True, primary_key = True)
    vk_id = Column(BigInteger, unique = True)

class BlackLists:
    __tablename__ = 'black__lists'

    id = Column(Integer, autoincrement = True, primary_key = True)
    user_id = Column(Integer,ForeignKey('users.id'))
    candidate_id = Column(Integer,ForeignKey('candidate.id'))

    users = relationship(Users, backref='black__lists')
    candidate = relationship(Candidate, backref='black__lists')

class Likes:
    __tablename__ = 'likes'

    id = Column(Integer, autoincrement = True, primary_key = True)
    user_id = Column(Integer,ForeignKey('users.id'))
    candidate_id = Column(Integer,ForeignKey('candidate.id'))
    
    users = relationship(Users, backref='likes')
    candidate = relationship(Candidate, backref='likes')

def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables (engine):
    Base.metadata.drop_all(engine)
