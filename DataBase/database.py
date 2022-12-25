import sqlalchemy
from sqlalchemy.orm import sessionmaker
from .model import Users, Candidate, BlackLists, Likes, Base

TABLE = {'Users': Users, 'Candidate': Candidate, 'BlackLists': BlackLists, 'Likes': Likes}


def get_engine (dbname, password, login='postgres'):

    DSN = f"postgresql://{login}:{password}@localhost:5432/{dbname}"
    engine = sqlalchemy.create_engine(DSN)
    return (engine)


def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop_all(engine)


def clear_db(engine):
    drop_tables(engine)
    create_tables(engine)


class Database:

    def __init__(self, engine) -> None:
        self.engin = engine
        Session = sessionmaker(bind=self.engin)
        self.session = Session()

    def add_user(self, vk_id: int, city: int, age: int, gender: int, count: int):
        result = Users(vk_id=vk_id, city=city, age=age, gender=gender, count=count)
        self.session.add(result)
        self.session.commit()

    def add_candidate (self,vk_id:int,city:int,age:int,gender:int):
        result = Candidate(vk_id = vk_id,city = city,age = age,gender = gender)
        self.session.add(result)
        # self.session.commit()

    def session_commit(self):
        self.session.commit()

    def add_like(self,user_id:int,candidate_id:int):
        result = Likes(user_id = user_id,candidate_id = candidate_id)
        self.session.add(result)
        self.session.commit()

    def add_black_list (self,user_id:int,candidate_id:int):
        result = BlackLists(user_id = user_id,candidate_id = candidate_id)
        self.session.add(result)
        self.session.commit()
        pass
    
    def find_date (self,table:str,search_function:str):
        """table: Users, Candidate, BlackLists, Likes"""
        find_result = self.session.query(TABLE[table]).filter(eval(search_function))
        find_result = find_result.all()
        return find_result

    def get_user_id(self, vk_id: int):
        result = self.session.query(Users).filter(Users.vk_id == vk_id)
        return result.all()[0].id

    def get_user_city(self, vk_id: int):
        result = self.session.query(Users).filter(Users.vk_id == vk_id)
        return result.all()[0].city

    def get_user_candidate_id(self, vk_id: int):
        result = self.session.query(Candidate).filter(Candidate.vk_id == vk_id)
        return result.all()[0].id

    def get_user_count(self, vk_id: int):

        result = self.session.query(Users).filter(Users.vk_id == vk_id)

        return result.all()[0].count if result.all() else None

    def get_candidate(self, city):

        result = self.session.query(Candidate.vk_id).filter(Candidate.city == city).all()
        for i in result:
            yield i[0]

    def check(self, table, vk_id:int):  

        """table: Users, Candidate, BlackLists, Likes"""
        result = self.session.query(TABLE[table]).filter(TABLE[table].vk_id == vk_id)
        res = self.session.query(result.exists()).scalar()
        return res

    def re_write(self, vk_id, count=None, city=None):

        id = self.get_user_id(vk_id=vk_id)

        i = self.session.query(Users).get(id)

        if city is not None:
            i.city = city
        if count is not None:
            i.count = count
        self.session.add(i)
        self.session.commit()
