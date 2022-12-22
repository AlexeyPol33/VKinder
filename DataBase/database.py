import sqlalchemy
from sqlalchemy.orm import sessionmaker
from model import *

def get_engine (dbname,password,login = 'postgres'):

    DSN = f"postgresql://{login}:{password}@localhost:5432/{dbname}"
    engine = sqlalchemy.create_engine(DSN)
    return(engine)

def clear_db(engine):
    drop_tables(engine)
    create_tables(engine)

class database ():
    def __init__(self,engine) -> None:
        self.engin = engine
        Session = sessionmaker(bind=self.engin)
        self.session = Session()

    def add_user (self,vk_id:int,city:int,age:int,gender:int):
        result = Users(vk_id = vk_id,city = city,age = age,gender = gender)
        self.session.add(result)
        self.session.commit()

    def add_candidate (self,vk_id:int,city:int,age:int,gender:int):
        result = Candidate(vk_id = vk_id,city = city,age = age,gender = gender)
        self.session.add(result)
        self.session.commit()

    def add_like (self,user_id:int,candidate_id:int):
        if (self.session.query(BlackLists).filter(BlackLists.user_id == user_id and BlackLists.candidate_id == candidate_id)).all():
            raise 'User in black list'
        if not self.session.query(Likes).filter(Likes.user_id == user_id and Likes.candidate_id == candidate_id):
            return
        result = Likes(user_id = user_id,candidate_id = candidate_id)
        self.session.add(result)
        self.session.commit()

    def add_black_list (self,user_id:int,candidate_id:int):
        result = BlackLists(user_id = user_id,candidate_id = candidate_id)
        self.session.add(result)
        self.session.commit()
        pass
    
    def find_date (self,table:object,search_function:str):
        find_result = self.session.query(table).filter(eval(search_function))
        find_result = find_result.all()
        return find_result

    def get_user_id(self,vk_id:int):
        result = self.find_date(Users,'Users.vk_id == vk_id')
        if result:
            return result[0].id
        else:
            return None

    def get_candidate_id(self,vk_id):
        result = self.find_date(Candidate,'Candidate.vk_id == vk_id')
        if result:
            return result[0].id
        else:
            return None
        
    def delete_user(self):
        pass

    def delete_candidate(self):
        pass

    def delete_like(self):
        pass

    def delete_black_list(self):
        pass

    def update_user(self):
        pass

    def update_candidate(self):
        pass


if __name__ == '__main__':
    engine = get_engine (dbname = '',password = '',login = 'postgres')
    create_tables(engine)
    
