import unittest

from users.models import User
from users.utils import get_user_info


class TestUserInfo(unittest.TestCase):


    def test_user_info(self):
        user = User.objects.get(username='pochikalin')
        access_token = 'ya29.a0ARrdaM8a5fd-0aUXQrLtNhRkM-6JMeNNMpOd_Zg-fEdnuzQvhqBantHnFaHaMg0i4czXUWNna7O51k7WE0b82npzPuaew3z6RoDSQHapP-7JD-DFvpToY5XLu-KxLL192w2ZzXXpvIBBVwKzgExYbKEjhxYL'
        get_user_info(access_token)

