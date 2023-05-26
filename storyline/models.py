"""Import django models for the project"""
from django.db import models
# This is the User model
from django.contrib.auth.models import User
# Import cloudinary for image processing
from cloudinary.models import CloudinaryField

# This is the cuple for published blog status
STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    """
    A model representing a blog post.

    Attributes:
        title (str): The title of the blog post.
        content (str): The content of the blog post.
        author (ForeignKey): The author of the blog post.
        created_date (DateTimeField): When the blog post was created.
        published_date (DateTimeField): When the blog post was published.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField("image", default="placeholder")
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name="blog_likes", blank=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """The records will be ordered by the created_on field in
            descending order (i.e., most recent first).
        """
        ordering = ["-created_on"]

    def __str__(self):
        return str(self.title)

    def number_of_likes(self):
        """"Returns the number of likes for the post."""
        return self.likes.count() if self.likes.exists() else 0

    def number_of_comments(self):
        """"Returns the number of comments for the post."""
        return self.comments.count() if self.comments.exists() else 0


class Comment(models.Model):
    """Represents a comment made by a user on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """The records will be ordered by the created_on field in
            ascending order.
        """
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
