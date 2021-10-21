import vk
from vk.exceptions import VkAPIError
from typing import List
import csv
import time

my_id = 312623584


class VkMainer():

    def __init__(self):
        with open('pass.txt', 'r') as pass_file: token = pass_file.readline().strip()
        self.session = vk.Session(access_token=token)
        self.api = vk.API(self.session)

    def get_friends(self, user_id: int, counter: int = 5000) -> List[int]:
        try:
            response = self.api.friends.get(user_id=user_id, count=counter, v='5.92')['items']
            time.sleep(0.3)
            return response
        except VkAPIError:
            time.sleep(0.3)
            return []

    def get_name(self, user_id: int) -> str:
        response = self.api.users.get(user_id=[user_id], v='5.92')[0]
        time.sleep(0.3)
        if 'deactivated' in response or response['is_closed']:
            return str(user_id)
        return response['first_name'] + "\n" + response['last_name']

    def friends_matrix(self, basic_user_id: int) -> List[List[int]]:
        close_friends = self.get_friends(basic_user_id)[:100]
        friends_lists = {basic_user_id: close_friends}
        nodes = set([basic_user_id] + close_friends)
        for friend in close_friends:
            friend_friends = self.get_friends(friend, counter=10)
            friends_lists[friend] = friend_friends
            nodes |= set(friend_friends)
        print('finished collecting')
        print(len(nodes), 'users data was collected')
        friends_dict = {id: ind + 1 for ind, id in enumerate(nodes)}
        matrix = [[0 for i in range(len(friends_dict) + 1)] for j in range(len(friends_dict) + 1)]
        for user_id in friends_dict:
            user_name = self.get_name(user_id)
            matrix[0][friends_dict[user_id]] = user_name
            matrix[friends_dict[user_id]][0] = user_name
        print("names fitted")
        for user_id in friends_lists:
            basic_ind = friends_dict[user_id]
            for friend in friends_lists[user_id]:
                aim_id = friends_dict[friend]
                matrix[basic_ind][aim_id] = 1
        return matrix


data_mainer = VkMainer()
data_matrix = data_mainer.friends_matrix(my_id)

with open('friendsgraph_small.csv', "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data_matrix)
