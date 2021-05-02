import datetime

import requests
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from urllib.parse import urlencode, urlunparse
from collections import OrderedDict


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    #api_url = f"https://api.vk.com/method/users.get?fields=bdate,sex,about&access_token={response['access_token']}&v=5.92"
    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_max_orig')), access_token=response['access_token'],
                                                v='5.92')),
                          None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex']:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    if data['bdata']:
        bdata = datetime.datetime.strptime(data['bdata'], '%d.%m.%Y').date()
        age = datetime.datetime.now().date().year - bdata.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    if data['photo_max_orig']:
        photo = requests.get(data['photo_max_orig'])
        if photo.status_code == 200:
            with open(f'media/users_avatars/{user.username}.jpg', 'wb') as f:
                f.write(photo.content)
                user.avatar = f'/users_avatars/{user.username}.jpg'

    user.save()