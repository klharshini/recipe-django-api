from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.contrib.auth.models import User
from .serializers import UserSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_user(username='', email='', last_name='', first_name='', password=''):
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name

    def setUp(self):
        self.create_user('harshini', 'harshini@gmail.com', 'pass')
        self.create_user('abcd', 'abcd@gmail.com', 'pass')
        self.create_user('ghjkl', 'ghjkl@gmail.com', 'pass')


class GetAllUserTest(BaseViewTest):
    def test_get_all_users(self):
        """
        Test to check all the users are returning.
        """
        response = self.client.get(
            reverse("users-all")
        )
        expected = User.objects.all()
        serialized = UserSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
