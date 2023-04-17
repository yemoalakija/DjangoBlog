"""
The Django Admin Site
This module provides the administrative interface for Django web applications.
It allows authorized users to create, view, edit, and delete content from the
application's database through a user-friendly interface. The admin site can
be customized by registering models and creating custom admin classes that
define how each model should be displayed and edited.
For more information, see the Django documentation:
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/
"""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment


# Register your models here.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """Prepopulated notes for the site"""
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("status", "created_on")
    list_display = ("title", "slug", "status", "created_on")
    search_fields = ["title", "content"]
    summernote_fields = ("content")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """User comment section model"""
    list_display = ("name", "body", "post", "created_on", "approved")
    list_filter = ("approved", "created_on")
    search_fields = ["name", "email", "body"]
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        """To approve reader comment"""
        queryset.update(approved=True)
