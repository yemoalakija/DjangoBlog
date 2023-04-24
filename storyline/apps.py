"""App config"""
from django.apps import AppConfig


class StorylineConfig(AppConfig):
    """Initialises app config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storyline'
