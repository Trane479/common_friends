from pprint import pprint
from urllib.parse import urlencode
import requests
from config import TOKEN
import time


class User:
    def __init__(self, token, char_id):
        self.token = token
        self.char_id = char_id

    def get_id(self):

        response = requests.get('https://api.vk.com/method/users.get',
                                params={
                                    'access_token': self.token,
                                    'user_ids': self.char_id,
                                    'v': '5.89'

                                })
        json_ = response.json()
        user_id = json_['response'][0]['id']
        return user_id

    def friends_get(self):
        user_id = self.get_id()
        response = requests.get('https://api.vk.com/method/friends.get',
                                params={
                                    'user_id': user_id,
                                    'access_token': self.token,
                                    'v': '5.8'
                                }
                                )
        json_ = response.json()
        friends = json_['response']['items']
        return friends

    def __and__(self, user):
        user_id = self.get_id()
        response = requests.get('https://api.vk.com/method/friends.getMutual',
                                params={
                                    'access_token': self.token,
                                    'source_uid': user_id,
                                    'target_uid': user.get_id(),
                                    'v': '5.89'

                                })
        json_ = response.json()
        return json_

    def __str__(self):
        return 'vk.com/' + str(self.char_id)


def show_mutual_friends(json_):
    mutual_ids = json_['response']
    mutual_friends = []
    for id in mutual_ids:
        mutual_friends.append(User(TOKEN, str(id)))

    if len(mutual_friends) == 0:
        print('Общих дурзей нет')
    else:
        print(f'Общих друзей - {len(mutual_friends)}:')
    for id in mutual_friends:
        time.sleep(0.4)
        print('vk.com/' + str(User.get_id(id)))


# user1 = User(TOKEN, 'traneisback')
# user2 = User(TOKEN, 'teslahu')
#
#
# show_mutual_friends(user1 & user2)
# print(user1)

def main():
    user1 = input('Введите  id первого пользователя:')
    user2 = input('Введите  id второго пользователя:')
    vkuser1 = User(TOKEN, user1)
    vkuser2 = User(TOKEN, user2)
    print(vkuser1, vkuser2)
    show_mutual_friends(vkuser1 & vkuser2)

main()