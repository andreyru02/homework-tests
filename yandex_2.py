from pprint import pprint
import requests
import config
from datetime import datetime
from time import sleep
import json
import sys


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token_vk, version):
        self.token_vk = token_vk
        self.version = version
        self.params = {
            'access_token': self.token_vk,
            'v': self.version
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    def get_photos(self, user_id=None, count=None, album_id='profile'):
        """
        Метод получает количество лайков и URL фотографий
        Возвращает dict {likes: {url: size}}
        """
        if user_id is None:
            user_id = self.owner_id
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': user_id,
            'album_id': album_id,
            'extended': 1,
            'count': count,
            'rev': 1
        }
        res = requests.get(photos_url, params={**self.params, **photos_params}).json()
        if 'error' in res:
            if res['error']['error_code'] == 200:
                sys.exit('Access denied!')
        elif len(res['response']['items']) == 0:
            sys.exit('Album is null!')

        #  получение url фотографий в макс. размере
        photo_url_dict = {}
        for photo in res['response']['items']:
            photo_url = photo['sizes'][-1]['url']
            likes = photo['likes']['count']
            size = photo['sizes'][-1]['type']
            if likes not in photo_url_dict:
                photo_url_dict[likes] = {photo_url: size}
            else:
                photo_url_dict[f"{likes}_{datetime.today().strftime(f'%Y%m%d')}"] = {photo_url: size}
        return photo_url_dict


class YaUploader(VkUser):
    def __init__(self, token_ya, token_vk, version):
        super().__init__(token_vk, version)
        self.token_ya = token_ya

    def create_folder(self, folder_name):
        """Метод создает папку для загрузки файла"""
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': self.token_ya}
        params = {'path': folder_name}
        resp = requests.put(url, params=params, headers=headers)
        if resp.status_code == 201:
            print(f'Folder {folder_name} created.')
            return folder_name
        elif resp.status_code == 409:
            # params = {'path': f"{folder_name}_{datetime.today().strftime(f'%Y%m%d')}"}
            # resp = requests.put(url, params=params, headers=headers)
            # print(f"Folder {folder_name}_{datetime.today().strftime(f'%Y%m%d')} created.")
            # return f"{folder_name}_{datetime.today().strftime(f'%Y%m%d')}"
            return resp.status_code

    def upload(self, user_id, count=5, album_id='profile'):
        """Метод загружает файл по URL на яндекс диск"""
        info = {'information': {'items': []}}
        url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        name_url_upload = self.get_photos(user_id, count, album_id)
        folder_name = self.create_folder(user_id)
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': self.token_ya}
        count_upload = 0
        for likes, value in name_url_upload.items():
            for url, size in value.items():
                file_dict = {}
                params = {
                    'path': str(folder_name) + '/' + str(likes) + '.jpg',
                    'url': url
                }
                resp = requests.post(url_upload, params=params, headers=headers)
                resp.raise_for_status()
                if resp.status_code == 202:
                    count_upload += 1
                    print(f'File {count_upload} of {len(name_url_upload)} uploaded.')
                    sleep(0.33)

                    # json
                    file_dict['file_name'] = str(likes) + '.jpg'
                    file_dict['size'] = size

                    info["information"]['items'].append(file_dict)
                    # сериализация
                    with open('json.json', 'w') as f:
                        json.dump(info, f, ensure_ascii=False, indent=2)
            # десериализация
        with open('json.json', encoding='utf-8') as f:
            data = json.load(f)
            pprint(data)


if __name__ == '__main__':
    upload = YaUploader(config.TOKEN_YA_DISK, config.TOKEN_VK, '5.130')
    upload.upload(1, count=10, album_id='saved')

# count - по дефолту 5.
# album_id - по дефолту profile.
# wall — фотографии со стены;
# profile — фотографии профиля;
# saved — сохраненные фотографии
