import os
import requests

VK_TOKEN = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
OAUTH_TOKEN = 'AQAAAAA6V87mAADLW1dKDlEyvUKgtP9prsHI_TY'
VK_URL = 'https://api.vk.com/method/photos.get'
HOST = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
BASE_PATH = os.getcwd()


def vk_params():
    return {
        'owner_id': 622400944,
        'access_token': VK_TOKEN,
        'v': '5.131',
        'album_id': 'profile',
        'type': 'post'
    }


def photo_get_url():
    params = vk_params()
    res = requests.get(VK_URL, params=params)
    return res.json()


def get_id():
    photo_id = []
    params = vk_params()
    res = requests.get(VK_URL, params=params).json()
    for i in res['response']['items']:
        photo_id.append(i['post_id'])
    return photo_id


def largest_photo_url():
    photos = photo_get_url()['response']['items']
    url_list = []
    size = []
    for item in photos:
        sizes = (item['sizes'][-1])
        url_list.append(sizes['url'])
        size.append(sizes['type'])
    return url_list


def get_likes():
    likes_count = []
    try:
        for id_ in get_id():
            params = {
                'owner_id': 622400944,
                'access_token': VK_TOKEN,
                'v': '5.131',
                'album_id': 'profile',
                'type': 'post',
                'item_id': f'{id_}'
            }
            res = requests.get('https://api.vk.com/method/likes.getList', params=params)
            likes_count.append(res.json()['response']['count'])
    except KeyError:
        pass
    return likes_count



