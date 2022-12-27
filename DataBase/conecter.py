from vk_requests import VK
from vk_bot import *
from datetime import date
import re

from tokens_file import dbname, password, access_token

_database = Database(engine=get_engine(dbname=dbname, password=password))
vk_request = VK(access_token=access_token)

class LikeBlacklist:
    _database = Database(engine=get_engine(dbname=dbname, password=password))
    def __init__(self) -> None:
        self.my_viewed_list = []
        pass

    def viewed_list(self,candidate_id):

        self.my_viewed_list.append(candidate_id)

        if len(self.my_viewed_list) > 2:
            del self.my_viewed_list[0]


    def like(self,user_id):

        count = _database.get_user_count(user_id) - 1
        city = _database.get_user_city(user_id)
        people = [people for people in _database.get_candidate(city)]
        candidate_id = people[count]
        _database.add_like(_database.get_user_id(user_id), _database.get_user_candidate_id(candidate_id))


    def black_list(self,user_id):

        count = _database.get_user_count(user_id) - 1
        city = _database.get_user_city(user_id)
        people = [people for people in _database.get_candidate(city)]
        candidate_id = people[count]
        _database.add_black_list(_database.get_user_id(user_id), _database.get_user_candidate_id(candidate_id))



def calculate_age(bdate):

    today = date.today()
    result = re.match(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", bdate)
    return today.year - int(result.group(3)) - ((today.month, today.day) < (int(result.group(2)), int(result.group(1))))


def insert(user_id, random_id, city=None):

    user_info = vk_request.users_info(user_id)
    city = user_info.get('city') if city is None else city  # TODO Возникает ошибка ключа
    gender = user_info['sex']
    bdate = user_info['bdate']
    age = calculate_age(bdate)
    candidate_gender = 1 if gender == 2 else 2

    people = vk_request.get_people(city=city, sex=candidate_gender,
                                   age_from=int(age)-1, age_to=int(age)+1)['response']['items']
    for candidate in people:
        if candidate['is_closed']:
            continue
        candidate_id = candidate['id']
        if 'city' in candidate:
            if candidate['city']['id'] == city:
                candidate_city = candidate['city']['id']
            else:
                continue
        else:
            continue
        if 'bdate' in candidate:
            candidate_bdate = candidate['bdate']
        else:
            continue
        # candidate_bdate = candidate['bdate']
        if len(candidate_bdate) in [8, 9, 10]:
            candidate_age = calculate_age(candidate_bdate)
        else:
            continue
        calculate_gender = candidate['sex']

        if not _database.check('Candidate', candidate_id):
            _database.add_candidate(vk_id=candidate_id, city=candidate_city,
                                    age=candidate_age, gender=calculate_gender)
            # print('кандидат добавлен')
        else:
            pass
            # print('кандидат уже есть')

    count = 1 # _database.session.query(Candidate.id).filter(Candidate.city == city)[0][0]

    if not _database.check('Users', user_id):
        _database.add_user(vk_id=user_id, city=city, age=age, gender=gender, count=count, random_id=random_id)
        print(f'Зареган новенький с id = { _database.get_user_id(user_id) }')
    else:
        print(f"Уже был и посмотрел до {_database.get_user_count(user_id)}")

    _database.session_commit()
