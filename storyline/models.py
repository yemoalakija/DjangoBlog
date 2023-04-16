from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    """
    A model representing a blog post.

    Attributes:
        title (str): The title of the blog post.
        content (str): The content of the blog post.
        author (ForeignKey): The author of the blog post, represented by a User model.
        created_date (DateTimeField): The date and time when the blog post was created.
        published_date (DateTimeField): The date and time when the blog post was published.
    """
    title = models.CharField(max_length=250, unique=True)
    title = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField("image", default="placeholder")
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name="blog_likes", blank=True)

    class Meta:
        """The records will be ordered by the created_on field in
            descending order (i.e., most recent first).
        """
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        """"Returns the number of likes for the post."""
        return self.likes.count()


class Comment(models.Model):
    """Represents a comment made by a user on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
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
        return (f"Comment {self.body} by {self.name}")
