from vk_api.longpoll import VkEventType

# --
from vk_bot import VkBot, longpoll
# --


if __name__ == '__main__':
    print("Server started")
    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                print(f'New message from {event.user_id}', end='')

                bot = VkBot(event.user_id)

                bot.write_msg(event.user_id, bot.new_message(event.text))

                print('Text: ', event.text)
                print("-------------------")