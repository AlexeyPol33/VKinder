import sqlalchemy
from sqlalchemy.orm import sessionmaker
from model import *

def get_engine (dbname,password,login = 'postgres'):

    DSN = f"postgresql://{login}:{password}@localhost:5432/{dbname}"
    engine = sqlalchemy.create_engine(DSN)
    return(engine)


class database ():
    def __init__(self,engine) -> None:
        self.engin = engine
        Session = sessionmaker(bind=self.engin)
        self.session = Session()

    def add_user (self,vk_id:int):
        result = Users(vk_id = vk_id)
        self.session.add(result)
        self.session.commit()

    def add_candidate (self,vk_id:int,city:str,age:int,gender:chr):
        if age < 18:
            return 'Возраст не может быть меньше 18'
        if gender != 'м' or gender != 'ж':
            return 'Не верный пол'
        result = Candidate(vk_id = vk_id,city = city,age = age,gender = gender)
        self.session.add(result)
        self.session.commit()

    def add_likes (self,user_id:int,candidate_id:int):
        result = Likes(user_id = user_id,candidate_id = candidate_id)
        self.session.add(result)
        self.session.commit()

    def add_black__lists (self,user_id:int,candidate_id:int):
        result = BlackLists(user_id = user_id,candidate_id = candidate_id)
        self.session.add(result)
        self.session.commit()
        pass
    
    def get_user_id(self,vk_id:int):
        result = self.session.query(Users).filter(Users.vk_id == vk_id)
        print(result.all()[0].id)


if __name__ == '__main__':
    engine = get_engine (dbname = '',password = '')
    create_tables(engine)

