from model import *
from database import *

data_users =   [{'vk_id':111111111,'city': 1, 'age':18,'gender':0},
                {'vk_id':222222222,'city': 2, 'age':19,'gender':1},
                {'vk_id':333333333,'city': 3, 'age':20,'gender':0},
                {'vk_id':444444444,'city': 4, 'age':21,'gender':1},]

data_candidate =   [{'vk_id':199999999,'city': 1, 'age':18,'gender':0},
                    {'vk_id':299999999,'city': 2, 'age':19,'gender':1},
                    {'vk_id':399999999,'city': 3, 'age':20,'gender':0},
                    {'vk_id':499999999,'city': 4, 'age':21,'gender':1},
                    {'vk_id':599999999,'city': 4, 'age':21,'gender':1},
                    {'vk_id':699999999,'city': 4, 'age':21,'gender':1},
                    {'vk_id':799999999,'city': 4, 'age':21,'gender':1},
                    {'vk_id':899999999,'city': 4, 'age':21,'gender':1},]

data_likes =   [{'user_id':1,'candidate_id':1},
                {'user_id':1,'candidate_id':2},
                {'user_id':2,'candidate_id':3},
                {'user_id':2,'candidate_id':4}]

data_black_lists =    [{'user_id':3,'candidate_id':5},
                        {'user_id':3,'candidate_id':6},
                        {'user_id':4,'candidate_id':7},
                        {'user_id':4,'candidate_id':8}]

def fill_the_database_with_test_data(database):
    db = database

    for du in data_users:
        db.add_user(**du)

    for dc in data_candidate:
        db.add_candidate(**dc)

    for dl in data_likes:
        db.add_likes(**dl)

    for dbl in data_black_lists:
        db.add_black_lists(**dbl)


if __name__ == '__main__':
    engine = get_engine(dbname = '',password = '')
    #clear_db(engine)
    db = database(engine)
    #fill_the_database_with_test_data(db)

    print(db.find_date(Users,'Users.vk_id == 111111111')[0])

    