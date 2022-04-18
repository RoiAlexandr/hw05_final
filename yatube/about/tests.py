from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class StaticPagesURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_About_exists_at_desired_location(self):
        """Проверка доступности адресовов."""
        page_list = {
            reverse('about:author'): HTTPStatus.OK,
            reverse('about:tech'): HTTPStatus.OK,
        }
        for address, status_code in page_list.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status_code)

    def test_pages_about_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'about/author.html': reverse('about:author'),
            'about/tech.html': reverse('about:tech'),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
