from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

# Настройки для обоих клавиатур
settings = dict(one_time=False, inline=True)

# №1. Клавиатура с 3 кнопками: "показать всплывающее сообщение", "открыть URL" и изменить меню (свой собственный тип)
keyboard_1 = VkKeyboard(**settings)
keyboard_1.add_callback_button(label='❌', color=VkKeyboardColor.SECONDARY, payload={"type": "my_own_100500_type_edit"})
keyboard_1.add_callback_button(label='❤', color=VkKeyboardColor.SECONDARY, payload={"type": "my_own_100500_type_edit"})


def get_but(text, color):
    return {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"" + "1" + "\"}",
                    "label": f"{text}"
                },
                "color": f"{color}"
            }
keyboard = {
    "one_time" : False,
    "buttons" : [
        [get_but('Старт', 'positive'), get_but('Время', 'positive')],
        [get_but('Привет', 'positive'), get_but('Пока', 'positive')]
    ]
}
keyboard = json.dumps(keyboard, ensure_ascii = False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
