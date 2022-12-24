from .database import Database, get_engine
from .model import Users, Candidate, create_tables

from vk_bot import *
from datetime import date
import re

from tokens_file import dbname, password

_database = Database(engine=get_engine(dbname = dbname,password = password))

def calculate_age(bdate):
    today = date.today()
    result = re.match(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", bdate)
    return today.year - int(result.group(3)) - ((today.month, today.day) < (int(result.group(2)), int(result.group(1))))

def createTable():
    engine = get_engine (dbname = dbname, password = password)
    create_tables(engine)



def insert(user_id):
    
    
    city = vk_request.users_info(user_id=user_id)['response'][0]['city']['id'] #TODO Возникает ошибка ключа
    gender = vk_request.users_info(user_id=user_id)['response'][0]['sex']
    bdate = vk_request.users_info(user_id=user_id)['response'][0]['bdate']
    age = calculate_age(bdate)

    candidate_gender = 1 if gender==2 else 2


    if not _database.check( Users, user_id):
        _database.add_user(vk_id=user_id, city=city, age=age, gender=gender, count=0)
        print(f'Зареган новенький с id = { _database.get_user_id(user_id) }')
    else:
        print(f"Уже был и посмотрел до {_database.get_user_count(user_id)}")
   



    for candidate in vk_request.get_people(city=city, sex=candidate_gender, age_from=int(age)-1,age_to=int(age)+1)['response']['items']:
        if candidate['is_closed']:
            continue
        candidate_id =  candidate['id']
        if 'city' in candidate:
            if candidate['city']['id'] == city:
                candidate_city = candidate['city']['id']
            else:
                continue
        else:
            continue
        candidate_bdate = candidate['bdate']
        if len(candidate_bdate) in [8,9,10]:
            candidate_age = calculate_age(candidate_bdate)
        else:
            continue
        calculate_gender = candidate['sex']

        if not _database.check(Candidate, candidate_id):
            _database.add_candidate( vk_id=candidate_id, city=candidate_city,age=candidate_age,gender=calculate_gender )
            # print('кандидат добавлен')
        else:
            pass
            # print('кандидат уже есть')
    _database.session_commit()


