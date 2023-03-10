from DataBase.database import *
from DataBase.conecter import insert, LikeBlacklist

from vk_package.vk_requests import VK

# vk_group_token - token from your group with access rights to messages
# access_token - token from your vk app
# group_id - id of your group
# dbname - name of your postgres DB
# password - password of your postgres DB
from tokens_file import vk_group_token, access_token, group_id, dbname, password

from buttons import keyboard_1, keyboard, city_keyboard, change_candidates_page

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll


GROUP_ID: int = group_id
GROUP_TOKEN = vk_group_token
API_VERSION = '5.131'

vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

vk_request = VK(access_token=access_token)

_database = Database(engine=get_engine(dbname=dbname, password=password))


class VkBot:

    def __init__(self, user_id, last_message_id):

        print("\nСоздан объект бота!")

        user_info = vk_request.users_info(user_id)
        self._USER_ID = user_id
        self._USERNAME = user_info['first_name']
        self._CITY = user_info.get('city')
        self.page_size = 5
        self.last_message_id = last_message_id
        self.like_black_list = LikeBlacklist()
        if self._CITY is None:
            if _database.check('Users', self._USER_ID):
                self._CITY = _database.get_user_city(self._USER_ID)
        else:
            self._CITY = self._CITY.get('id')

        self._COMMANDS = ["ПРИВЕТ", "ВРЕМЯ", "ПОКА", "НАЧАТЬ", 'BLACK_LIST', 'LIKE', 'ИЗБРАННОЕ']

    def insert_data(self, city_id=None):

        if city_id is None:
            insert(user_id=self._USER_ID, last_message_id=self.last_message_id, city=self._CITY)
        else:
            self._CITY = city_id
            insert(user_id=self._USER_ID, last_message_id=self.last_message_id, city=self._CITY)

    def new_message(self, message):

        if 'город' in message.lower():
            home_town = message.lower().replace('город', '').strip()
            cities = self.get_cities(home_town=home_town)
            if cities:
                page_size = self.page_size
                message_keyboard = city_keyboard(cities=cities, home_town=home_town, page_size=page_size).get_keyboard()
                return {'message': f'Выберите нужный город:', 'keyboard': message_keyboard}
            else:
                return {'message': 'Город не найден, повсторите попытку'}

        # Привет
        elif message.upper() == self._COMMANDS[0]:

            return {"message": f"Привет-привет, {self._USERNAME}!", 'keyboard': keyboard}

        # Пока
        elif message.upper() == self._COMMANDS[2]:

            return {"message": f"Пока, {self._USERNAME}(", 'keyboard': keyboard}

        # Начать, like, black_list
        elif message.upper() in (self._COMMANDS[3], self._COMMANDS[4], self._COMMANDS[5]):
            print('получение кандидатов')

            if not _database.check('Users', self._USER_ID):
                if self._CITY is None:
                    return {'message': 'Чтобы начать работу отправьте сообщение <<Город "Название города">>',
                            'keyboard': keyboard}
                self.insert_data()
            count = _database.get_user_count(self._USER_ID) - 1
            people = [people for people in _database.get_candidate(user_id=self._USER_ID)]
            find_candidate_id = people[count]
            self.like_black_list.viewed_list(find_candidate_id)
            user_info = vk_request.users_info(find_candidate_id)
            first_name = user_info['first_name']
            last_name = user_info['last_name']
            link = f'https://vk.com/id{find_candidate_id}'
            photos = vk_request.get_popular_photo(find_candidate_id)
            photos = ','.join(photos)
            message_keyboard = keyboard_1.get_keyboard()

            return {"message": f'{first_name} {last_name}\n{link}', 'attachment': photos,
                    'keyboard': message_keyboard}

        # Избранное
        elif message.upper() == self._COMMANDS[6]:
            message_keyboard = change_candidates_page(self.page_size).get_keyboard()
            _candidats_ids = _database.find_date('Likes', f'Likes.user_id == {_database.get_user_id(self._USER_ID)}')
            if not _candidats_ids:
                return {'message': 'Вы пока никого не добавили', 'keyboard': message_keyboard}
            _candidats_ids = [i.candidate_id for i in _candidats_ids]
            _candidats_vk_id = []
            for candidate_id in _candidats_ids:
                _candidat = _database.find_date('Candidate', f'Candidate.id == {candidate_id}')[0]
                _candidats_vk_id.append(_candidat.vk_id)
            _candidate_info = []
            start = self.page_size - 5
            end = self.page_size
            for i in range(start, end):
                if i not in range(len(_candidats_vk_id)):
                    pass
                else:
                    _user_info = vk_request.users_info(_candidats_vk_id[i])
                    _first_name = _user_info['first_name']
                    _last_name = _user_info['last_name']
                    _link = f'https://vk.com/id{_candidats_vk_id[i]}'
                    _candidate_info.append(f'{_first_name} {_last_name}: {_link}')
            _candidate_info = 'Избранное:\n' + '\n'.join(_candidate_info) if _candidate_info \
                else 'Вы ушли слишком далеко)'

            return {"message": f'{_candidate_info}', 'keyboard': message_keyboard}

        else:
            if not _database.check('Users', self._USER_ID):

                return {"message": 'Для начала нажмите кнопку "Начать.\nИли отправьте сообщение со словом "Начать"',
                        'keyboard': keyboard}

            message_text = "Не понимаю о чем вы...\n" \
                           "Вот скисок команд:\n" \
                           "Привет - приветствие от бота;\n" \
                           "Пока - прощание от бота;\n" \
                           "Начать - запуск приложения;\n" \
                           "Избранное - показ кандидатов из списка понравившихся;"

            return {"message": message_text, 'keyboard': keyboard}

    @staticmethod
    def get_cities(home_town: str) -> list:

        city_name = home_town
        cities = vk_request.get_cities_id(city_name)['response']['items']

        return cities

    def get_last_message_id(self) -> int:
        last_id = _database.get_last_message_id(self._USER_ID)

        return last_id
