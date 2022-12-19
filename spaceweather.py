import requests
import re
from bs4 import BeautifulSoup


def create_map():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.5112.124 YaBrowser/22.9.4.863 Yowser/2.5 Safari/537.36'
    }
    url = 'https://www.spaceweatherlive.com/images/grafieken/aurora-map2.jpg'
    response = requests.get(url, headers=headers)
    aurora = response.content
    # with open('aurora_map_3.jpg', 'wb') as jpg:
    #     jpg.write(aurora)
    #     print('Done')
    return aurora


def create_table():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.5112.124 YaBrowser/22.9.4.863 Yowser/2.5 Safari/537.36'
    }
    url = 'https://www.spaceweatherlive.com/ru/otchety/prognoz-na-3-dnya.html'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    quotes = soup.find_all('pre')
    kp_table = str(quotes[0]).split('\n')
    new_kp_table = []
    # with open('kp_table.txt', 'w') as table:
    #     for i in range(2, len(kp_table) - 2):
    #         if i == 2:
    #             table.write(f'            {kp_table[i].strip()}\n')
    #         else:
    #             table.write(f'{kp_table[i].strip()}\n')
    for i in range(2, len(kp_table) - 2):
        if i == 2:
            line = kp_table[i].strip()
            line = re.sub(r'\s+', ' ', line)
            new_kp_table.append(f'Дата   {line}')
        else:
            line = kp_table[i].strip()
            line = re.sub(r'\s+', ' ', line)
            new_kp_table.append(f'{line}')
    print('Done')
    return "\n".join(new_kp_table)