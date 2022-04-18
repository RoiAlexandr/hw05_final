from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

User = get_user_model()


# Тестирование шаблонов и контекста
class UserVIEWSTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Sasha')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
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
            reverse('users:password_reset_confirm',
                    args=('uid64', 'token')):
            'users/password_reset_confirm.html',
            reverse('users:password_reset_complete'):
            'users/password_reset_complete.html',
            reverse('users:logout'): 'users/logged_out.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_signup_form_page_show_correct_context(self):
        """Проверьте, что в контексте передаётся форма
         для создания нового пользователя."""
        response = self.authorized_client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
