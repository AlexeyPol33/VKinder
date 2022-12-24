from DataBase.database import *
from DataBase.model import Users, Candidate
from DataBase.like_blacklist import viewed_list
from DataBase.conecter import insert

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

_database = Database(engine=get_engine(dbname=dbname, password=password))


class VkBot:

    def __init__(self, user_id):
        print("\nСоздан объект бота!")

        self._USER_ID = user_id
        self._USERNAME = vk_request.users_info(user_id)['first_name']
        self._CITY = vk_request.users_info(user_id)['city']['id']

        self._COMMANDS = ["ПРИВЕТ", "ВРЕМЯ", "ПОКА", "НАЧАТЬ", 'BLACK_LIST', 'LIKE']

    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:

            return {"message": f"Привет-привет, {self._USERNAME}!"}

        # Время
        elif message.upper() == self._COMMANDS[1]:

            return {"message": f"{self._get_time()}"}

        # Пока
        elif message.upper() == self._COMMANDS[2]:
            # clear_db(engine=get_engine(dbname=dbname, password=password))

            return {"message": f"Пока, {self._USERNAME}("}

        # Фото
        elif message.upper() in (self._COMMANDS[3], self._COMMANDS[4], self._COMMANDS[5]):

            print('получение кандидатов')

            if not _database.check('Users', self._USER_ID):
                insert(self._USER_ID)
            count = _database.get_user_count(self._USER_ID) - 1
            city = self._CITY
            people = [people for people in _database.get_candidate(city)]
            find_user_id = people[count]

            viewed_list(find_user_id)
            first_name = vk_request.users_info(find_user_id)['first_name']
            last_name = vk_request.users_info(find_user_id)['last_name']
            link = f'https://vk.com/id{find_user_id}'
            photos = vk_request.get_popular_photo(find_user_id)
            photos = ','.join(photos)

            return {"message": f'{first_name} {last_name}\n{link}', 'attachment': photos,
                    'keyboard': keyboard_1.get_keyboard()}

        elif message.upper() == 'ОЧИСТИТЬ':
            clear_db(get_engine(dbname=dbname, password=password))

            return {"message": "Таблица очищена"}

        else:
            if not _database.check('Users', self._USER_ID):

                return {"message": 'Для начала нажмите кнопку "Начать.\nИли отправьте сообщение со словом "Начать"',
                        'keyboard': keyboard}

            return {"message": "Не понимаю о чем вы..."}

    @staticmethod
    def _get_time():

        date = datetime.datetime.now().strftime("%d.%m.%Y")
        time = datetime.datetime.now().strftime("%H:%M")
        now = f'Текущая дата: {date}\nТекущее время: {time}'

        return now
