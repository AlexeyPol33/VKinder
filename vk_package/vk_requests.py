import requests
import random
import time


class VK:

    def __init__(self, access_token, version='5.131'):
        self._token = access_token
        self.version = version
        self.params = {'access_token': self._token, 'v': self.version}

    def my_id(self):

        return requests.get('https://api.vk.com/method/users.get', params=self.params).json()['response'][0]['id'] 

    def users_info(self, user_id) -> dict:
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id, 
                  'fields': 'sex, city, bdate'}
        response = requests.get(url, params={**self.params, **params})
        res = response.json()
        time.sleep(0.2)
        return res['response'][0]

    def get_photo(self, user_id, album_id='profile') -> dict:
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id, 'album_id': album_id, 'photo_sizes': 1, 'extended': 1}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_popular_photo(self, user_id) -> list:
        photos = self.get_photo(user_id)
        while True:
            if 'error' in photos:
                photos = self.get_photo(user_id)
            else:
                break
        most_popular_photos = sorted(photos['response']['items'], key=lambda x: x['likes']['count'], reverse=True)
        photos = []
        if most_popular_photos:
            owner_id = most_popular_photos[0]['owner_id']
            if len(most_popular_photos) < 3:
                for i in range(len(most_popular_photos)):
                    photo = f'photo{owner_id}_{most_popular_photos[i]["id"]}'
                    photos.append(photo)
            else:
                for i in range(3):
                    photo = f'photo{owner_id}_{most_popular_photos[i]["id"]}'
                    photos.append(photo)
        return photos

    def get_people(self, city, sex, age_from, age_to) -> dict:
        url = 'https://api.vk.com/method/users.search'
        params = {'fields': 'sex, city, bdate', 'city': city, 'sex': sex,
                  'age_from': age_from, 'age_to': age_to, 'count': 1000}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_cities_id(self, city_name) -> dict:
        url = 'https://api.vk.com/method/database.getCities'
        params = {'country_id': 1, 'q': city_name}
        response = requests.get(url=url, params={**self.params, **params})
        return response.json()
