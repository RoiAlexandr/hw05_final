from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from ..models import Group, Post
from http import HTTPStatus

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testslug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем общедоступные страницы
    def test_guest_client_url_exists_at_desired_location(self):
        """Проверка доступности адресовов guest_client."""
        page_list = {
            reverse('posts:index'): HTTPStatus.OK,
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug}): HTTPStatus.OK,
            reverse('posts:profile', kwargs={'username': self.user.username}):
                HTTPStatus.OK,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                HTTPStatus.OK
        }
        for address, status_code in page_list.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status_code)

    def test_authorized_client_url_exists_at_desired_location(self):
        """Проверка доступности адресовов authorized_client."""
        page_list = {
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
                HTTPStatus.OK,
            reverse('posts:post_create'): HTTPStatus.OK,
            '/unexisting_page/': HTTPStatus.NOT_FOUND
        }
        for address, status_code in page_list.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, status_code)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
                'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',

        }
        for address, template in templates_url_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
