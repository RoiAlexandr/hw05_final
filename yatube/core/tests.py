from django.test import TestCase, Client
from django.contrib.auth import get_user_model


User = get_user_model()


class PagesURLTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='auth')
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_404_url_uses_correct_template(self):
        """Проверка, что страница 404 отдает кастомный шаблон."""
        response = self.guest_client.get('/core/404/')
        self.assertTemplateUsed(response, 'core/404.html')
