import sqlalchemy
from sqlalchemy.orm import sessionmaker
from .model import *

def get_engine (dbname,password,login = 'postgres'):

    DSN = f"postgresql://{login}:{password}@localhost:5432/{dbname}"
    engine = sqlalchemy.create_engine(DSN)
    return(engine)



class Database():
    def __init__(self, engine) -> None:
        self.engin = engine
        Session = sessionmaker(bind=self.engin)
        self.session = Session()

    def add_user(self,vk_id:int,city:int,age:int,gender:int, count:int):
        result = Users(vk_id = vk_id,city = city,age = age,gender = gender, count=count)
        self.session.add(result)
        self.session.commit()





    def add_candidate (self,vk_id:int,city:int,age:int,gender:int):
        result = Candidate(vk_id = vk_id,city = city,age = age,gender = gender)
        self.session.add(result)
        # self.session.commit()
    
    
    def session_commit(self):
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
        return result.all()[0].id


    def get_user_candidate_id(self,vk_id:int):
        result = self.session.query(Candidate).filter(Candidate.vk_id == vk_id)
        return result.all()[0].id


    def get_user_count(self,vk_id:int):
        result = self.session.query(Users).filter(Users.vk_id == vk_id)
        return result.all()[0].count



    def get_candidate(self, *args):

        result = self.session.query(*args)

        for i in result:
            yield i


    def check(self, table, vk_id:int):
        result = self.session.query(table).filter(table.vk_id == vk_id)
        res = self.session.query(result.exists()).scalar()
        return res


    def re_write(self, vk_id, count):

        id = self.get_user_id(vk_id=vk_id)

        i = self.session.query(Users).get(id)

        i.count = count
        self.session.add(i)
        self.session.commit()




# if __name__ == '__main__':
#     engine = get_engine (dbname = 'vkTinder',password = '1234')
#     create_tables(engine)



   
   