from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse

User = get_user_model()


class UserURLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Sasha')
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_guest_client_url_exists_at_desired_location(self):
        """Проверка доступности адресовов guest_client."""
        page_list = {
            reverse('users:signup'): HTTPStatus.OK,
            reverse('users:login'): HTTPStatus.OK,
            reverse('users:password_change'): HTTPStatus.FOUND,
            reverse('users:password_change_done'): HTTPStatus.FOUND,
            reverse('users:password_reset'): HTTPStatus.OK,
            reverse('users:password_reset_confirm', args={'uidb64', 'token'}):
                HTTPStatus.OK,
        }
        for address, status_code in page_list.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status_code)

    def test_authorized_client_url_exists_at_desired_location(self):
        """Проверка доступности адресовов authorized_client."""
        page_list = {
            reverse('users:password_change_done'): HTTPStatus.OK,
            reverse('users:password_reset_done'): HTTPStatus.OK,
            reverse('users:password_reset_complete'): HTTPStatus.OK,
            reverse('users:logout'): HTTPStatus.OK,
        }
        for address, status_code in page_list.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, status_code)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:password_change'):
                'users/password_change_form.html',
            reverse('users:password_change_done'):
                'users/password_change_done.html',
            reverse('users:password_reset'):
                'users/password_reset_form.html',
            reverse('users:password_reset_done'):
                'users/password_reset_done.html',
            reverse('users:password_reset_confirm', args={'uidb64', 'token'}):
                'users/password_reset_confirm.html',
            reverse('users:password_reset_complete'):
                'users/password_reset_complete.html',
            reverse('users:logout'): 'users/logged_out.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
