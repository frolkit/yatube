from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile

from yatube import settings
from .models import Post, Group

User = get_user_model()

@override_settings(CACHES=settings.TEST_CACHES)
class PostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@example.com',
            password="12345")
        self.client.login(username='test_user', password='12345')
        self.test_text = 'test text..'
        self.edit_text = 'edit text..'

    def test_create_profile(self):
        response = self.client.get("/test_user/")
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post(
            "/new/",
            {"text": self.test_text},
            follow=True)
        self.assertContains(response, self.test_text)

    def test_create_post_without_login(self):
        self.client.get("/auth/logout/")
        response = self.client.post(
            "/new/",
            {"text": self.test_text},
            follow=True)
        self.assertContains(response, "Пожалуйста, авторизуйтесь.")

    def test_post(self):
        post = Post.objects.create(author=self.user, text=self.test_text)
        response_index = self.client.get("/")
        response_profile = self.client.get("/test_user/")
        response_post = self.client.get(f"/test_user/{post.id}/")
        self.assertContains(response_index, self.test_text)
        self.assertContains(response_profile, self.test_text)
        self.assertContains(response_post, self.test_text)

    def test_post_edit(self):
        post = Post.objects.create(author=self.user, text=self.test_text)
        self.client.post(
            f"/test_user/{post.id}/edit/",
            {"text": self.edit_text},
            follow=True)
        response_index = self.client.get("/")
        response_profile = self.client.get("/test_user/")
        response_post = self.client.get(f"/test_user/{post.id}/")
        self.assertContains(response_index, self.edit_text)
        self.assertContains(response_profile, self.edit_text)
        self.assertContains(response_post, self.edit_text)

    def test_404_page(self):
        response = self.client.get("/not/exist/page/")
        self.assertEqual(response.status_code, 404)

@override_settings(CACHES=settings.TEST_CACHES)
class ImageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@example.com',
            password="12345")
        self.client.login(username='test_user', password='12345')
        self.group = Group.objects.create(title='test_title', slug='test_slug')
        with open('media/posts/test.jpg', mode='rb') as img:
            self.response_post = self.client.post(
                "/new/",
                {'text': "текст", "group": self.group.id, 'image': img},
                follow=True)

    def test_image_post(self):
        self.assertContains(self.response_post, '<img')

    def test_image_index_profile_group(self):
        response_index = self.client.get("/")
        response_profile = self.client.get("/test_user/")
        response_group = self.client.get("/group/test_slug/")
        self.assertContains(response_index, '<img')
        self.assertContains(response_profile, '<img')
        self.assertContains(response_group, '<img')

    def test_image_format_file(self):
        with open('media/posts/test.txt', mode='rb') as img:
            response = self.client.post(
                "/new/",
                {'text': "текст", "group": self.group.id, 'image': img},
                follow=True)
        self.assertContains(response, 'Upload a valid image.')

@override_settings(CACHES=settings.TEST_CACHES)
class FollowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user_follower',
            email='user_follower@example.com',
            password="12345")
        self.client.login(username='user_follower', password='12345')
        self.author = User.objects.create_user(
            username='user_following',
            email='user_following@example.com',
            password="12345")
        self.post_user = Post.objects.create(author=self.user,
                                             text="Просто текст")
        self.post_author = Post.objects.create(author=self.author,
                                               text="Избранный текст")

    def test_follow_and_unfollow(self):
        follow = self.client.get('/user_following/follow/', follow=True)
        unfollow = self.client.get('/user_following/unfollow/', follow=True)
        self.assertContains(follow, "Подписчиков: 1")
        self.assertContains(unfollow, "Подписчиков: 0")

    def test_posts_in_follow_index(self):
        self.client.get('/user_following/follow/', follow=True)
        response = self.client.get('/follow/')
        self.assertContains(response, "Избранный текст")
        self.assertNotContains(response, "Просто текст")

    def test_add_comment_without_login(self):
        self.client.get("/auth/logout/", follow=True)
        response = self.client.post(
            f"/user_following/{self.post_user.id}/comment/",
            {'text': 'пробный коммент'},
            follow=True)
        self.assertContains(response, "Пожалуйста, авторизуйтесь.")


class CacheTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@example.com',
            password="12345")
        self.client.login(username='user_follower', password='12345')
        self.post = Post.objects.create(author=self.user, text="Просто текст")
        self.client.get('/')
    
    def test_index_cache(self):
        self.post.text = 'изменённый текст'
        self.post.save()
        response = self.client.get('/')
        self.assertContains(response, "Просто текст")
