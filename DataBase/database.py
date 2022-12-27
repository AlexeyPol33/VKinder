import sqlalchemy
from sqlalchemy.orm import sessionmaker
from .model import Users, Candidate, BlackLists, Likes, Base

TABLE = {'Users': Users, 'Candidate': Candidate, 'BlackLists': BlackLists, 'Likes': Likes}


def get_engine(dbname, password, login='postgres'):

    DSN = f"postgresql://{login}:{password}@localhost:5432/{dbname}"
    engine = sqlalchemy.create_engine(DSN)
    return engine


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

    def add_user(self, vk_id: int, city: int, age: int, gender: int, count: int, last_message_id: int):
        result = Users(vk_id=vk_id, city=city, age=age, gender=gender, count=count, last_message_id=last_message_id)
        self.session.add(result)
        self.session.commit()

    def add_candidate(self, vk_id: int, city: int, age: int, gender: int):
        result = Candidate(vk_id=vk_id, city=city, age=age, gender=gender)
        self.session.add(result)

    def session_commit(self):
        self.session.commit()

    def add_like(self, user_id: int, candidate_id: int):
        find_black = self.find_date('BlackLists', f'(BlackLists.user_id == {user_id}) & '
                                                  f'(BlackLists.candidate_id == {candidate_id})')
        find_like = self.find_date('Likes', f'(Likes.user_id == {user_id}) & (Likes.candidate_id == {candidate_id})')
        if not find_like:
            result = Likes(user_id=user_id, candidate_id=candidate_id)
            self.session.add(result)
            self.session.commit()
        if find_black:
            self.session.query(BlackLists).filter((BlackLists.user_id == user_id) &
                                                  (BlackLists.candidate_id == candidate_id)).delete()
            self.session.commit()

    def add_black_list(self, user_id: int, candidate_id: int):
        find_black = self.find_date('BlackLists', f'(BlackLists.user_id == {user_id}) & '
                                                  f'(BlackLists.candidate_id == {candidate_id})')
        find_like = self.find_date('Likes', f'(Likes.user_id == {user_id}) & (Likes.candidate_id == {candidate_id})')
        if not find_black:
            result = BlackLists(user_id=user_id, candidate_id=candidate_id)
            self.session.add(result)
            self.session.commit()
        if find_like:
            self.session.query(Likes).filter((Likes.user_id == user_id) & (Likes.candidate_id == candidate_id)).delete()
            self.session.commit()
    
    def find_date(self, table: str, search_function: str):
        """table: Users, Candidate, BlackLists, Likes"""
        find_result = self.session.query(TABLE[table]).filter(eval(search_function))
        find_result = find_result.all()
        return find_result

    def get_user_id(self, vk_id: int):
        result = self.session.query(Users).filter(Users.vk_id == vk_id).all()
        return result[0].id if result else None

    def get_user_city(self, vk_id: int):
        result = self.session.query(Users).filter(Users.vk_id == vk_id)
        return result.all()[0].city

    def get_user_age(self, vk_id: int):
        result = self.session.query(Users).filter(Users.vk_id == vk_id)
        return result.all()[0].age

    def get_user_gender(self, vk_id: int):
        result = self.session.query(Users).filter(Users.vk_id == vk_id)
        return result.all()[0].gender

    def get_user_candidate_id(self, vk_id: int):
        result = self.session.query(Candidate).filter(Candidate.vk_id == vk_id)
        return result.all()[0].id

    def get_user_count(self, vk_id: int):

        result = self.session.query(Users).filter(Users.vk_id == vk_id)

        return result.all()[0].count if result.all() else None

    def get_candidate(self, user_id):

        city = self.get_user_city(vk_id=user_id)
        age = self.get_user_age(vk_id=user_id)
        gender = self.get_user_gender(vk_id=user_id)
        gender = 1 if gender == 2 else 2

        likes = self.find_date('Likes',
                               f'Likes.user_id == {self.get_user_id(user_id)}')
        likes = [i.candidate_id for i in likes]
        black_list = self.find_date('BlackLists',
                                    f'BlackLists.user_id == {self.get_user_id(user_id)}')
        black_list = [i.candidate_id for i in black_list]
        union_list = likes + black_list
        result = self.session.query(
            Candidate.vk_id,
            Candidate.id,
            Candidate.age).filter(Candidate.city == city,
                                  Candidate.gender == gender).all()
        for i in result:
            if i[1] not in union_list and i[2] in (age-1, age, age+1):
                yield i[0]

    def get_last_message_id(self, vk_id: int):
        result = self.session.query(Users).filter(Users.vk_id == vk_id)
        return result[0].last_message_id if result.all() else None

    def check(self, table, vk_id: int):

        """table: Users, Candidate, BlackLists, Likes"""
        result = self.session.query(TABLE[table]).filter(TABLE[table].vk_id == vk_id)
        res = self.session.query(result.exists()).scalar()
        return res

    def re_write(self, vk_id, count=None, city=None, last_message_id=None):

        user_id = self.get_user_id(vk_id=vk_id)

        i = self.session.query(Users).get(user_id)

        if last_message_id is not None:
            i.last_message_id = last_message_id
        if city is not None:
            i.city = city
        if count is not None:
            i.count = count
        self.session.add(i)
        self.session.commit()
