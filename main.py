import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# --
from vk_bot import VkBot
from token import vk_token
# --


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})


# API-ключ созданный ранее
token = vk_token

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

print("Server started")
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            print(f'New message from {event.user_id}', end='')

            bot = VkBot(event.user_id)

            write_msg(event.user_id, bot.new_message(event.text))

            print('Text: ', event.text)
            print("-------------------")
