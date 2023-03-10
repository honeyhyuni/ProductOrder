from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import User


class SignupTests(APITestCase):
    """
        회원가입 테스트 케이스
    """
    def setUp(self):
        self.url = reverse('signup')
        self.client = APIClient()

    def test_create_user_success(self):
        """
        User 회원가입 성공 Test
        """
        data = {
            'email': 'test01@naver.com',
            'name': '이승현',
            'password': 'test0101!@',
            'check_password': 'test0101!@',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(email='test01@naver.com').exists())
        self.assertEqual(response.data['message']['msg'], 'You have successfully registered as a member!')

    def test_create_user_omission_check_password(self):
        """
            User 회원가입 check_password 누락시
        """
        data = {
            'email': 'test01@naver.com',
            'name': '이승현',
            'password': 'test0101!@',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertFalse(User.objects.filter(email='test01@naver.com').exists())

    def test_create_user_not_normalization_password(self):
        """
            User password 정규화 되지 않았을시
        """
        data = {
            'email': 'test01@naver.com',
            'name': '이승현',
            'password': 'test010101',
            'check_password': 'test010101'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertFalse(User.objects.filter(email='test01@naver.com').exists())

    def test_create_user_different_check_password(self):
        """
                   User check_password 다른값 들어왔을시
               """
        data = {
            'email': 'test01@naver.com',
            'name': '이승현',
            'password': 'test010101!@',
            'check_password': 'test010101!'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertFalse(User.objects.filter(email='test01@naver.com').exists())

    def test_create_user_exists(self):
        """
            이미 존재하는 email 로 회원가입 했을시
        """
        data = {
            'email': 'test01@naver.com',
            'name': '이승현',
            'password': 'test0101!@',
            'check_password': 'test0101!@',
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(email='test01@naver.com').exists())

        response2 = self.client.post(self.url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)