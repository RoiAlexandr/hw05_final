import shutil
import tempfile

from django.test import Client, TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.conf import settings
from posts.models import Post, Group, Comment
from django.contrib.auth import get_user_model
User = get_user_model()

# Создаем временную папку для медиа-файлов;
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

# временная папка TEMP_MEDIA_ROOT, а потом мы ее удалим


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем пользователя
        cls.author = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testslug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовая пост',
            group=cls.group,
        )
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_post(self):
        """Валидная форма создает пост."""
        # Подсчитаем количество постов
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый заголовок',
            'image': uploaded,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:profile', kwargs={
            'username': self.author.username}))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        form_data = {
            'text': 'Тестовый заголовок новый'
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={
                'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:post_detail', kwargs={
            'post_id': self.post.id}))
        # Проверяем, что пост отредактирован
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый заголовок новый',
            ).exists()
        )

    def test_create_comment_authorized_client(self):
        """Валидная форма создает коммент."""
        form_data = {
            'text': 'Тестовый комментарий',
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={
                'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:post_detail', kwargs={
            'post_id': self.post.id}))

        self.assertTrue(
            Comment.objects.filter(
                text='Тестовый комментарий',
            ).exists()
        )

    def test_create_comment_guest_client(self):
        """Не авторизованный пользователь не может создать коммент."""
        form_data = {
            'text': 'Тестовый комментарий',
        }
        # Отправляем POST-запрос
        self.guest_client.post(
            reverse('posts:add_comment', kwargs={
                'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        # Проверяем, что guest_client не добавил комментарий
        self.assertEqual(Comment.objects.count(), 0)
