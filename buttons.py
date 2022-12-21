from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# Настройки для обоих клавиатур
settings = dict(one_time=False, inline=True)

# №1. Клавиатура с 3 кнопками: "показать всплывающее сообщение", "открыть URL" и изменить меню (свой собственный тип)
keyboard_1 = VkKeyboard(**settings)
keyboard_1.add_callback_button(label='❌', color=VkKeyboardColor.SECONDARY, payload={"type": "my_own_100500_type_edit"})
keyboard_1.add_callback_button(label='❤', color=VkKeyboardColor.SECONDARY, payload={"type": "my_own_100500_type_edit"})
