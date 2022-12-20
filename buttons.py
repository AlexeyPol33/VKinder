from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# Настройки для обоих клавиатур
settings = dict(one_time=False, inline=True)

# №1. Клавиатура с 3 кнопками: "показать всплывающее сообщение", "открыть URL" и изменить меню (свой собственный тип)
keyboard_1 = VkKeyboard(**settings)
# pop-up кнопка
keyboard_1.add_callback_button(label='Покажи pop-up сообщение', color=VkKeyboardColor.SECONDARY, payload={"type": "show_snackbar", "text": "Это исчезающее сообщение"})
keyboard_1.add_line()
# кнопка с URL
keyboard_1.add_callback_button(label='Откртыть Url', color=VkKeyboardColor.POSITIVE, payload={"type": "open_link", "link": "https://vk.com/dev/bots_docs_5"})
keyboard_1.add_line()
# кнопка переключения на 2ое меню
keyboard_1.add_callback_button(label='Добавить красного ', color=VkKeyboardColor.PRIMARY, payload={"type": "my_own_100500_type_edit"})

# №2. Клавиатура с одной красной callback-кнопкой. Нажатие изменяет меню на предыдущее.
keyboard_2 = VkKeyboard(**settings)
# кнопка переключения назад, на 1ое меню.
keyboard_2.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE, payload={"type": "my_own_100500_type_edit"})