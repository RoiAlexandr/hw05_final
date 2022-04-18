from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()


class UserFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_create_user(self):
        """Валидная форма создает нового пользователя."""
        # Подсчитаем количество пользователй
        users_count = User.objects.count()
        form_data = {
            'first_name': 'Александр',
            'last_name': 'Рой',
            'username': 'Alex',
            'email': 'mail@yandex.ru',
            'password1': 'U61212fefefre4324',
            'password2': 'U61212fefefre4324',
        }
        # Отправляем POST-запрос
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:index',))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(User.objects.count(), users_count + 1)
