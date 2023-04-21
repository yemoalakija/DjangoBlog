"""Ddefines a new urls path"""
from django.urls import path
from . import views


urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("<slug>:slug/", views.PostDetail.as_view(), name="post_detail"),
]