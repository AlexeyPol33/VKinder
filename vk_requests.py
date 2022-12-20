import requests
import random


class VK:

    def __init__(self, access_token, version='5.131'):
        self._token = access_token
        self.version = version
        self.params = {'access_token': self._token, 'v': self.version}

    def users_info(self, user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_user_name(self, user_id):
        name = self.users_info(user_id)['response'][0]['first_name']
        surname = self.users_info(user_id)['response'][0]['last_name']
        return name, surname

    def get_photo(self, user_id, album_id='profile', count=1):
        id = user_id
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': id, 'album_id': album_id, 'photo_sizes': 1, 'extended': 1}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_popular_photo(self, user_id):
        photos = self.get_photo(user_id)
        while True:
            if 'error' in photos:
                photos = self.get_photo(user_id)
            else:
                break
        most_popular_photos = sorted(photos['response']['items'], key=lambda x: x['likes']['count'], reverse=True)
        owner_id = most_popular_photos[0]['owner_id']
        photos = []
        if len(most_popular_photos) < 3:
            for i in range(len(most_popular_photos)):
                photo = f'photo{owner_id}_{most_popular_photos[i]["id"]}'
                photos.append(photo)
        else:
            for i in range(3):
                photo = f'photo{owner_id}_{most_popular_photos[i]["id"]}'
                photos.append(photo)
        return photos

    def get_people(self):
        url = 'https://api.vk.com/method/users.search'
        params = {'city': 1, 'sex': 1, 'age_from': 20, 'age_to': 21, 'count': 1000}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def send_message(self, user_id, message):
        url = 'https://api.vk.com/method/messages.send'
        params = {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)}
        response = requests.put(url, params={**self.params, **params})
