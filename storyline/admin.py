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
from .models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """Docstring"""
    summernote_fields = ("content")
