from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotEventType
from buttons import city_keyboard

# --
from vk_bot import vk, VkBot, longpoll
# --

from DataBase.like_blacklist import *
from DataBase.database import *
from tokens_file import dbname, password

if __name__ == '__main__':

    pages = ['<<', '>>']
    engine = get_engine(dbname=dbname, password=password)
    _database = Database(engine=engine)
    create_tables(engine=engine)

    print("Server started")
    for event in longpoll.listen():

        # отправляем меню 1го вида на любое текстовое сообщение от пользователя
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message['text'] != '':
                if event.from_user:
                    print(f'New message from {event.obj.message["from_id"]}', end='')
                    # Если клиент пользователя не поддерживает callback-кнопки,
                    # нажатие на них будет отправлять текстовые
                    # сообщения. Т.е. они будут работать как обычные inline кнопки.
                    if 'callback' not in event.obj.client_info['button_actions']:
                        print(f'Клиент {event.obj.message["from_id"]} не поддерж. callback')

                    random_id = get_random_id()
                    user_id = event.obj.message['from_id']
                    user_text = event.obj.message['text']
                    bot = VkBot(user_id, random_id)
                    new_message = bot.new_message(user_text)
                    message_text = new_message.get('message')
                    message_attachment = new_message.get('attachment')
                    message_keyboard = new_message.get('keyboard')

                    last_id = vk.messages.send(
                        user_id=user_id,
                        random_id=random_id,
                        peer_id=user_id,
                        keyboard=message_keyboard,
                        message=message_text,
                        attachment=message_attachment)

                    last_message_id = event.obj['message']['conversation_message_id'] + 1
                    if _database.check('Users', user_id):
                        _database.re_write(vk_id=user_id, last_message_id=last_message_id)
                    print('Text: ', event.obj.message['text'])
                    print("-------------------")

        # обрабатываем клики по callback кнопкам
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            user_id = event.obj.peer_id
            try:
                bot = VkBot(user_id, random_id=event.obj.conversation_message_id)

                # если это одно из 3х встроенных действий:
                if isinstance(event.object.payload.get('type'), int):
                    # отправляем серверу указания как какую из кнопок обработать. Это заложено в
                    # payload каждой callback-кнопки при ее создании.
                    # Но можно сделать иначе: в payload положить свои собственные
                    # идентификаторы кнопок, а здесь по ним определить
                    # какой запрос надо послать. Реализован первый вариант.

                    home_town = event.object.payload.get('home')
                    cities = bot.get_cities(home_town=home_town)
                    message_keyboard = city_keyboard(cities=cities, home_town=home_town,
                                                     page_size=bot.page_size * event.object.payload.get('type'))

                    last_id = vk.messages.edit(
                        peer_id=user_id,
                        message='Выберите город:',
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=message_keyboard.get_keyboard())

                # если это наша "кастомная" (т.е. без встроенного действия) кнопка, то мы можем
                # выполнить edit сообщения и изменить его меню. Но при желании мы могли бы
                # на этот клик открыть ссылку/приложение или показать pop-up. (см.анимацию ниже)
                elif event.object.payload.get('type') == 'like':
                    print(f'New calling button from {event.obj.peer_id}')
                    print(f'New calling message: {event.obj.message_id}')
                    print(f'New calling message: {event.obj.conversation_message_id}')
                    if event.obj.conversation_message_id == bot.get_last_message_id():

                        like(user_id)
                        count = _database.get_user_count(user_id)
                        count += 1
                        _database.re_write(user_id, count=count)
                        user_text = event.object.payload.get('type')
                        new_message = bot.new_message(user_text)
                        message_text = new_message.get('message')
                        message_attachment = new_message.get('attachment')
                        message_keyboard = new_message.get('keyboard')

                        last_id = vk.messages.edit(
                            peer_id=user_id,
                            message=message_text,
                            attachment=message_attachment,
                            conversation_message_id=event.obj.conversation_message_id,
                            keyboard=message_keyboard)

                        print(f'Call button: {event.object.payload.get("type")}')
                        print("-------------------")
                    else:
                        random_id = get_random_id()
                        message_text = 'Данное сообщение устарело. Нажмите "Начать"'

                        last_id = vk.messages.send(
                            user_id=user_id,
                            random_id=random_id,
                            peer_id=user_id,
                            message=message_text)

                        last_message_id = bot.get_last_message_id() + 1
                        if _database.check('Users', user_id):
                            _database.re_write(vk_id=user_id, last_message_id=last_message_id)

                elif event.object.payload.get('type') == 'black_list':
                    print(f'New calling button from {event.obj.peer_id}')
                    print(f'New calling message: {event.obj.conversation_message_id}')
                    if event.obj.conversation_message_id == bot.get_last_message_id():

                        black_list(user_id)
                        count = _database.get_user_count(user_id)
                        count += 1
                        _database.re_write(user_id, count=count)
                        user_text = event.object.payload.get('type')
                        new_message = bot.new_message(user_text)
                        message_text = new_message.get('message')
                        message_attachment = new_message.get('attachment')
                        message_keyboard = new_message.get('keyboard')

                        last_id = vk.messages.edit(
                            peer_id=user_id,
                            message=message_text,
                            attachment=message_attachment,
                            conversation_message_id=event.obj.conversation_message_id,
                            keyboard=message_keyboard)

                        print(f'Call button: {event.object.payload.get("type")}')
                        print("-------------------")
                    else:
                        random_id = get_random_id()
                        message_text = 'Данное сообщение устарело. Нажмите "Начать"'

                        last_id = vk.messages.send(
                            user_id=user_id,
                            random_id=random_id,
                            peer_id=user_id,
                            message=message_text)

                        last_message_id = bot.get_last_message_id() + 1
                        if _database.check('Users', user_id):
                            _database.re_write(vk_id=user_id, last_message_id=last_message_id)

                else:
                    city = event.object.payload.get('type')
                    home_town = event.object.payload.get('home')
                    CITIES = {city['title']: city['id'] for city in bot.get_cities(home_town=home_town)}
                    city = CITIES[city]
                    bot.insert_data(city_id=city)
                    _database.re_write(vk_id=user_id, count=1, city=city)

                    new_message = bot.new_message("Начать")
                    message_text = new_message.get('message')
                    message_attachment = new_message.get('attachment')
                    message_keyboard = new_message.get('keyboard')

                    last_id = vk.messages.edit(
                        peer_id=user_id,
                        message=message_text,
                        attachment=message_attachment,
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=message_keyboard)

            except KeyError:
                random_id = get_random_id()

                last_id = vk.messages.edit(
                    peer_id=user_id,
                    message=f"Что-то пошло не так(\nПопробуйте начать сначала.",
                    conversation_message_id=event.obj.conversation_message_id,)
