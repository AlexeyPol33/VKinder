from DataBase.database import *
from DataBase.model import Users, Candidate
from DataBase.like_blacklist import viewed_list

from vk_requests import VK
from tokens_file import vk_group_token, access_token, group_id, dbname, password
import datetime
# import random

from buttons import keyboard_1, keyboard

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll

# from data import peoples

# Общие
GROUP_ID = group_id
GROUP_TOKEN = vk_group_token
API_VERSION = '5.131'

# виды callback-кнопок
CALLBACK_TYPES = ('show_snackbar', 'open_link')

# Запускаем бот
vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

vk_request = VK(access_token=access_token)

_database = Database(engine=get_engine(dbname = dbname, password = password))


class VkBot:

    def __init__(self, user_id):
        print("\nСоздан объект бота!")

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ВРЕМЯ", "ПОКА", "СТАРТ", 'ВПРАВО']


    def _get_user_name_from_vk_id(self, user_id):
        name = vk_request.get_user_name(user_id)[0]
        return name

    def new_message(self, message):


        if message.upper() == 'НАЧАТЬ':
            # people = vk_request.get_people()['response']['items']
            # users = {'users': []}
            # for user in people:
            #     if not user['is_closed']:
            #         users['users'].append(user['id'])
            # with open('users_data.json', encoding='utf-8', mode='a') as users_file:
            #     json.dump(users, users_file, indent=4, ensure_ascii=False)
            return {"message": 'Можно начинать!', 'keyboard': keyboard}

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return {"message": f"Привет-привет, {self._USERNAME}!"}

        # Время
        elif message.upper() == self._COMMANDS[1]:
            return {"message": f"{self._get_time()}"}

        # Пока
        elif message.upper() == self._COMMANDS[2]:
            return {"message": f"Пока, {self._USERNAME}("}

        # Фото
        elif message.upper() in (self._COMMANDS[3], self._COMMANDS[4]):
            
            # people = [people[0] for people in peoples()]


            people = [people[0] for people in _database.get_candidate(Candidate.vk_id)]
            
            print('получение кандидатов')
            

            # people = [user['id'] for user in vk_request.get_people(1,2,21,22)['response']['items'] if not user['is_closed']]
            # find_user_id = random.choice(people)
            # counter_candidate = _database.get_user_counter(self._USER_ID)


            count = _database.get_user_count(self._USER_ID)
            find_user_id = people[count]
            count += 1 
            _database.re_write(self._USER_ID, count=count)
    
            
           
            viewed_list(find_user_id)


            name = ' '.join(vk_request.get_user_name(find_user_id))
            link = f'https://vk.com/id{find_user_id}'
            photos = vk_request.get_popular_photo(find_user_id)
            photos = ','.join(photos)
            return {"message": f'{name}\n{link}', 'attachment': photos, 'keyboard': keyboard_1.get_keyboard()}

        else:
            return {"message": "Не понимаю о чем вы..."}

    @staticmethod
    def _get_time():
        date = datetime.datetime.now().strftime("%d.%m.%Y")
        time = datetime.datetime.now().strftime("%H:%M")
        now = f'Текущая дата: {date}\nТекущее время: {time}'
        return now
