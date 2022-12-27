from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

# Настройки для обоих клавиатур
settings = dict(one_time=False, inline=True)

# №1. Клавиатура с 3 кнопками: "показать всплывающее сообщение", "открыть URL" и изменить меню (свой собственный тип)
keyboard_1 = VkKeyboard(**settings)
keyboard_1.add_callback_button(label='❌', color=VkKeyboardColor.SECONDARY, payload={"type": "black_list"})
keyboard_1.add_callback_button(label='❤', color=VkKeyboardColor.SECONDARY, payload={"type": "like"})


def change_candidates_page(page_size: int):

    keyboard_3 = VkKeyboard(**settings)
    keyboard_3.add_callback_button(label="<<", color=VkKeyboardColor.SECONDARY,
                                   payload={"type": 'change_page', "size": (page_size - 5) // 5})
    keyboard_3.add_callback_button(label=">>", color=VkKeyboardColor.SECONDARY,
                                   payload={"type": 'change_page', "size": (page_size + 5) // 5})

    return keyboard_3


def city_keyboard(cities: list, home_town: str, page_size: int):

    start = page_size - 5
    end = page_size

    keyboard_2 = VkKeyboard(**settings)
    if start < 0 or end < 0:
        pass
    else:
        for i in range(start, end):
            if i <= len(cities) - 1:
                city = cities[i]['title']
                region = cities[i].get('region', 'РФ')
                keyboard_2.add_callback_button(label=f"{city}, {region}", color=VkKeyboardColor.SECONDARY,
                                               payload={"type": f"{cities[i]['title']}", "home": home_town})
                keyboard_2.add_line()
            elif i < 0:
                break
            else:
                break
    keyboard_2.add_callback_button(label="<<", color=VkKeyboardColor.SECONDARY,
                                   payload={"type": (page_size - 5) // 5, "home": home_town})
    keyboard_2.add_callback_button(label=">>", color=VkKeyboardColor.SECONDARY,
                                   payload={"type": (page_size + 5) // 5, "home": home_town})

    return keyboard_2


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
    "one_time": False,
    "buttons": [
        [get_but('Начать', 'positive'), get_but('Избранное', 'positive')],
        [get_but('Привет', 'positive'), get_but('Пока', 'positive')]
    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
