from tokens_file import dbname, password

from .database import Database, get_engine


_database = Database(engine=get_engine(dbname=dbname, password=password))


my_viewed_list = []


def viewed_list(candidate_id):

    my_viewed_list.append(candidate_id)

    if len(my_viewed_list) > 2:
        del my_viewed_list[0]


def like(user_id):

    count = _database.get_user_count(user_id) - 1
    people = [people for people in _database.get_candidate(user_id=user_id)]
    candidate_id = people[count]
    _database.add_like(_database.get_user_id(user_id), _database.get_user_candidate_id(candidate_id))


def black_list(user_id):

    count = _database.get_user_count(user_id) - 1
    people = [people for people in _database.get_candidate(user_id=user_id)]
    candidate_id = people[count]
    _database.add_black_list(_database.get_user_id(user_id), _database.get_user_candidate_id(candidate_id))