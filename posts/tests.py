from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from .models import Post, Group

User = get_user_model()


class SimpleTest(TestCase):
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
        self.assertContains(response, "Вы обратились к странице, доступ к которой возможен только для залогиненных пользователей.")

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


class Image(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@example.com',
            password="12345")
        self.client.login(username='test_user', password='12345')
        self.group = Group.objects.create(title='test_title', slug='test_slug')     
        with open('media/posts/test_mne_zapili.jpg') as img:
            self.client.post('new/', {'text': 'fred', 'image': img})

    def test_image_post(self):
        response = self.client.get("/")
        self.assertContains(response, 'gdfgf')

    def test_image_index_profile_group(self):
        pass
    
    def test_image_format_file(self):
        pass

        