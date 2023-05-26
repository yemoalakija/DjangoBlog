"""Defines django crispy_forms"""
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """Initialises comment form"""
    # pylint: disable=too-few-public-methods
    class Meta:
        """Defines form model and field"""
        model = Comment
        fields = ("body",)

    def clean_body(self):
        """Ensure comment body is not empty or whitespace-only"""
        body = self.cleaned_data["body"]
        if not body.strip():
            raise forms.ValidationError("Comment cannot be empty or contain only whitespace.")
        return body
