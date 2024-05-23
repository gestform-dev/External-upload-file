from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from paperless.serialisers import UserSerializer
from paperless.views import EditProfileView, EditPasswordView
from django.contrib.auth import get_user_model

User = get_user_model()


class EditProfileViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='test@file.com', email='test@example.com')
        self.view = EditProfileView.as_view()

    def test_patch_with_valid_data(self):
        data = {'username': 'newusername@file.com', 'email': 'newusername@file.com'}
        request = self.factory.patch('edit-profile/', data)
        request.user = self.user

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newusername@file.com')

    def test_patch_with_null_data(self):
        data = {'username': '', 'email': ''}
        request = self.factory.patch('edit-profile/', data)
        request.user = self.user
        # breakpoint()
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_patch_with_invalid_data(self):
        data = {'username': 'zzzzz', 'email': 'zzzzz'}
        request = self.factory.patch('edit-profile/', data)
        request.user = self.user
        # breakpoint()
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)


class EditPasswordViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('oldpassword')
        self.user.save()
        self.view = EditPasswordView.as_view()

    def test_patch_with_valid_data_and_correct_old_password(self):
        data = {
            'password': 'oldpassword',
            'newPassword': 'newPassword1',
            }
        request = self.factory.patch('edit-password/', data)
        request.user = self.user

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password('newPassword1'))

    def test_patch_with_invalid_old_password(self):
        data = {
            'password': 'wrongpassword',
            'newPassword': 'newPassword1',
            }
        request = self.factory.patch('edit-password/', data)
        request.user = self.user

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_with_invalid_new_password(self):
        data = {
            'password': 'oldpassword',
            'newPassword': 'short',
            }
        request = self.factory.patch('edit-password/', data)
        request.user = self.user

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('newPassword', response.data)
