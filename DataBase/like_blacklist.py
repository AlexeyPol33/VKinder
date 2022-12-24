from tokens_file import dbname, password

from .database import Database, get_engine
from .model import Candidate


_database = Database(engine=get_engine(dbname=dbname, password=password))


my_viewed_list = []


def viewed_list(id):
    my_viewed_list.append(id)

    if len(my_viewed_list) > 2:
        del my_viewed_list[0]

    # print(my_viewed_list)


def like(user_id):
    count = _database.get_user_count(user_id)
    userid = _database.session.query(Candidate.vk_id).filter(Candidate.id == count)[0][0]
    # print(f'я {_database.get_user_id(user_id)}, Мне нравиться {_database.get_user_candidate_id(my_viewed_list[-2])}')
    _database.add_like(_database.get_user_id(user_id), _database.get_user_candidate_id(userid))


def black_list(user_id):
    count = _database.get_user_count(user_id)
    userid = _database.session.query(Candidate.vk_id).filter(Candidate.id == count)
    # print(f'я {_database.get_user_id(user_id)}, Мне не нравиться {_database.get_user_candidate_id(my_viewed_list[-2])}')
    _database.add_black_list(_database.get_user_id(user_id), _database.get_user_candidate_id(userid))