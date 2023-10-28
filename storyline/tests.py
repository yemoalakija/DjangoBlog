"""Test cases."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post


# Create test here
class BlogAppTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a test post
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post content.",
            author=self.user,
            status=1,
        )
        self.post.slug = "test-post"
        self.post.save()

    def test_post_list_view(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_post_detail_view(self):
        response = self.client.get(reverse("post_detail", args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertContains(response, "This is a test post content.")

    def test_post_like_view(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Send a POST request to like the post
        response = self.client.post(
            reverse("post_like", args=[self.post.slug]), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # Check if the post is liked
        liked = response.json()["liked"]
        self.assertTrue(liked)

        # Send a POST request to unlike the post
        response = self.client.post(
            reverse("post_like", args=[self.post.slug]), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # Check if the post is unliked
        liked = response.json()["liked"]
        self.assertFalse(liked)
