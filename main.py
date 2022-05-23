import os
import requests
from progress.bar import IncrementalBar
from VK_API import get_likes
from VK_API import largest_photo_url


VK_TOKEN = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
OAUTH_TOKEN = ''
VK_URL = 'https://api.vk.com/method/photos.get'
HOST = 'https://cloud-api.yandex.net/v1/disk/resources/upload/'
BASE_PATH = os.getcwd()


class YaDiskLoader():

    def __init__(self, oauth_token: str, host: str, base_path: str, yandex_save_foalder: str):
        self.oauth_token = oauth_token
        self.host = host
        self.base_path = base_path
        self.yandex_save_foalder = yandex_save_foalder

    def get_ya_headers(self):
        return {
            'Content-type': 'application/json',
            'Authorization': f'OAuth {self.oauth_token}',
        }

    def create_ya_folder(self):
        headers = self.get_ya_headers()
        params = {'path': f'{self.yandex_save_foalder}'}
        res = requests.put('https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=headers)
        return res

    def ya_link(self,):
        link_list = []
        self.create_ya_folder()
        for number in get_likes():
            params = {'path': f'{self.yandex_save_foalder}/{number}.jpg', 'overwrite': True}
            res = requests.get(url=HOST, params=params,  headers=self.get_ya_headers())
            link_list.append(res.json()['href'])
        return link_list



    def loader(self):
        photo_count = 0
        link_list = self.ya_link()
        headers = self.get_ya_headers()
        bar = IncrementalBar('Countdown', max=len(link_list))
        for item in link_list:
            bar.next()
            photo = requests.get(largest_photo_url()[photo_count])
            requests.put(item, data=photo, headers=headers)
            photo_count += 1
        bar.finish()


if __name__ == '__main__':
    yadisk = YaDiskLoader(OAUTH_TOKEN, HOST, BASE_PATH, 'img1')
    print(yadisk.loader())
