"""Defines django crispy_forms"""
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """Initialises comment form"""
    class Meta:
        """Defines form model and field"""
        model = Comment
        fields = ("body",)
