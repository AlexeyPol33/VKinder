from vk_requests import VK
from tokens_file import vk_token, access_token
import datetime
import random

from buttons import keyboard_1, keyboard_2
import vk_api
from vk_api.longpoll import VkLongPoll

vk_request = VK(access_token=access_token)

# API-ключ созданный ранее
token = vk_token

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)


class VkBot:

    def __init__(self, user_id):
        print("\nСоздан объект бота!")

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ВРЕМЯ", "ПОКА", "ФОТО"]

    def _get_user_name_from_vk_id(self, user_id):
        name = vk_request.get_user_name(user_id)[0]
        return name

    def new_message(self, message):

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
        elif message.upper() == self._COMMANDS[3]:
            people = vk_request.get_people()['response']['items']
            find_user_id = people[random.randint(0, len(people))]['id']
            name = ' '.join(vk_request.get_user_name(find_user_id))
            link = f'https://vk.com/id{find_user_id}'
            photos = vk_request.get_popular_photo(find_user_id)
            photos = ','.join(photos)
            return {"message": f'{name}\n{link}', 'attachment': photos}

        else:
            return {"message": "Не понимаю о чем вы..."}

    # def send_new_message(self, user_id, message):
    #     vk_request.send_message(user_id, message)

    @staticmethod
    def _get_time():
        date = datetime.datetime.now().strftime("%d.%m.%Y")
        time = datetime.datetime.now().strftime("%H:%M")
        now = f'Текущая дата: {date}\nТекущее время: {time}'
        return now

    @staticmethod
    def write_msg(user_id, message):
        params = {'user_id': user_id, 'random_id': random.randint(0, 2048)}
        res = vk.method('messages.send', {**params, **message})
        print(res)

    # @staticmethod
    # def send_attachment(user_id):
    #     find_user_id = 42549021 # vk_request.get_people()['response']['items'][random.randint(0, 1000)]['id']
    #     photos = vk_request.get_popular_photo(find_user_id)
    #     photos = ','.join(photos)
    #     vk.method('messages.send',
    #               {'user_id': user_id,
    #                'attachment': photos,
    #                'random_id': random.randint(0, 2048)})
