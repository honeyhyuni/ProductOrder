from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accounts.models import User


class AccountsTests(APITestCase):
    """
        로그인 로그아웃 테스트 케이스
    """

    @classmethod
    def setUpClass(cls):
        super(AccountsTests, cls).setUpClass()
        cls.url = reverse('login')
        cls.client = APIClient()
        cls.client.post(reverse('signup'), {'email': 'test01@naver.com', 'name': '이승현', 'password': 'testtest01!@',
                                            'check_password': 'testtest01!@'})
        user = cls.client.post(reverse('login'), {'email': 'test01@naver.com', 'password': 'testtest01!@'})
        cls.jwt = user.data['token']['access']

    def test_login_success(self):
        """
            로그인 성공시
        """
        data = {
            'email': 'test01@naver.com',
            'password': 'testtest01!@',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message']['msg'], 'login success')
        self.assertIsNotNone(response.data['token']['access'])
        self.assertIsNotNone(response.data['token']['refresh'])

    def test_login_fail(self):
        """
            로그인 실패시
        """
        data = {
            'email': 'test01@naver.com',
            'password': 'testtest01',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], '존재하지 않은 유저입니다.')

    def test_logout_success(self):
        """
            로그아웃 성공시
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt)
        response = self.client.post(reverse('logout'), format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['message'], 'Logout success')

    def test_logout_fail(self):
        """
            인증이 허가되지 않은 유저가 로그아웃에 접근시
        """
        response = self.client.post(reverse('logout'), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
