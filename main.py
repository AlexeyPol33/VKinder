from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotEventType
import json

# --
from vk_bot import vk, VkBot, longpoll, CALLBACK_TYPES
# --


if __name__ == '__main__':

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

                    user_id = event.obj.message['from_id']
                    user_text = event.obj.message['text']
                    bot = VkBot(user_id)
                    new_message = bot.new_message(user_text)
                    message_text = new_message.get('message')
                    message_attachment = new_message.get('attachment')
                    message_keyboard = new_message.get('keyboard')

                    vk.messages.send(
                        user_id=user_id,
                        random_id=get_random_id(),
                        peer_id=user_id,
                        keyboard=message_keyboard,
                        message=message_text,
                        attachment=message_attachment)

                    print('Text: ', event.obj.message['text'])
                    print("-------------------")

        # обрабатываем клики по callback кнопкам
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            # если это одно из 3х встроенных действий:
            if event.object.payload.get('type') in CALLBACK_TYPES:
                # отправляем серверу указания как какую из кнопок обработать. Это заложено в
                # payload каждой callback-кнопки при ее создании.
                # Но можно сделать иначе: в payload положить свои собственные
                # идентификаторы кнопок, а здесь по ним определить
                # какой запрос надо послать. Реализован первый вариант.
                r = vk.messages.sendMessageEventAnswer(
                    event_id=event.object.event_id,
                    user_id=event.object.user_id,
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload))
            # если это наша "кастомная" (т.е. без встроенного действия) кнопка, то мы можем
            # выполнить edit сообщения и изменить его меню. Но при желании мы могли бы
            # на этот клик открыть ссылку/приложение или показать pop-up. (см.анимацию ниже)
            elif event.object.payload.get('type') == 'my_own_100500_type_edit':
                print(f'New calling button from {event.obj.peer_id}')
                print(f'New calling message: {event.obj.conversation_message_id}', end='')

                user_id = event.obj.peer_id
                user_text = 'вправо'
                bot = VkBot(user_id)
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