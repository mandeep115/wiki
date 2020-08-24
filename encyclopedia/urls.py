from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="titles"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("random", views.random_page, name="random"),
    path("edit/<str:title>", views.edit, name="edit")
]
