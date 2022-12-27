from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotEventType
from buttons import keyboard, city_keyboard, change_candidates_page

# --
from vk_package.vk_bot import vk, VkBot, longpoll
# --
from DataBase.conecter import LikeBlacklist

from DataBase.database import *
from tokens_file import dbname, password

if __name__ == '__main__':

    like_black_list = LikeBlacklist()
    pages = ['<<', '>>']
    engine = get_engine(dbname=dbname, password=password)
    _database = Database(engine=engine)
    create_tables(engine=engine)

    print("Server started")
    for event in longpoll.listen():

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
                    bot = VkBot(user_id, last_message_id=random_id)
                    new_message = bot.new_message(user_text)
                    message_text = new_message.get('message')
                    message_attachment = new_message.get('attachment')
                    message_keyboard = new_message.get('keyboard')

                    if user_text == 'Начать':
                        pre_last_id = vk.messages.send(
                            user_id=user_id,
                            random_id=get_random_id(),
                            peer_id=user_id,
                            keyboard=keyboard,
                            message='Вот кандидаты')
                        last_message_id = event.obj['message']['conversation_message_id'] + 2
                    else:
                        last_message_id = event.obj['message']['conversation_message_id'] + 1
                    last_id = vk.messages.send(
                        user_id=user_id,
                        random_id=random_id,
                        peer_id=user_id,
                        keyboard=message_keyboard,
                        message=message_text,
                        attachment=message_attachment)

                    if _database.check('Users', user_id):
                        _database.re_write(vk_id=user_id, last_message_id=last_message_id)
                    print('Text: ', event.obj.message['text'])
                    print("-------------------")

        # обрабатываем клики по callback кнопкам
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            user_id = event.obj.peer_id
            try:
                bot = VkBot(user_id, last_message_id=event.obj.conversation_message_id)

                if event.object.payload.get('type') == 'change_page':

                    print(f'New callback from {user_id}')
                    print(f'Change favorite page')
                    bot.page_size = bot.page_size * event.object.payload.get('size')
                    page_size = bot.page_size
                    user_text = 'Избранное'
                    new_message = bot.new_message(user_text)
                    message_text = new_message['message']
                    message_keyboard = change_candidates_page(
                        page_size=page_size
                    )

                    last_id = vk.messages.edit(
                        peer_id=user_id,
                        message=message_text,
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=message_keyboard.get_keyboard())
                    print("-------------------")

                elif isinstance(event.object.payload.get('type'), int):

                    print(f'New callback from {user_id}')
                    print(f'Change city page')
                    bot.page_size = bot.page_size * event.object.payload.get('type')
                    page_size = bot.page_size
                    home_town = event.object.payload.get('home')
                    cities = bot.get_cities(home_town=home_town)
                    message_text = 'Выберите нужный город:' if (page_size - 5) in range(len(cities)) \
                        else 'Вы ушли слишком далеко)'
                    message_keyboard = city_keyboard(
                        cities=cities,
                        home_town=home_town,
                        page_size=page_size
                    ).get_keyboard()

                    last_id = vk.messages.edit(
                        peer_id=user_id,
                        message=message_text,
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=message_keyboard)
                    print("-------------------")

                elif event.object.payload.get('type') == 'like':

                    print(f'New callback from {event.obj.peer_id}')
                    print(f'Calling message: {event.obj.conversation_message_id}')
                    if event.obj.conversation_message_id == bot.get_last_message_id():

                        like_black_list.like(user_id)
                        count = _database.get_user_count(user_id)
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

                    print(f'New callback from {event.obj.peer_id}')
                    print(f'Calling message: {event.obj.conversation_message_id}')
                    if event.obj.conversation_message_id == bot.get_last_message_id():

                        like_black_list.black_list(user_id)
                        count = _database.get_user_count(user_id)
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

                        print(f'New callback from {event.obj.peer_id}')
                        print(f'Calling old message: {event.obj.conversation_message_id}')
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

                        print("-------------------")

                else:

                    print(f'New callback from {event.obj.peer_id}')
                    print(f'Change city')
                    print(f'Calling message: {event.obj.conversation_message_id}')
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

                    print("-------------------")

            except KeyError:

                print(f'New callback from {event.obj.peer_id}')
                print(f'Error: too many responses')
                random_id = get_random_id()

                last_id = vk.messages.edit(
                    peer_id=user_id,
                    message=f"Что-то пошло не так(\nПопробуйте начать сначала.",
                    conversation_message_id=event.obj.conversation_message_id,)

                print("-------------------")
