from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newPage", views.newPage, name="newPage"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("randomentry", views.randomEntry, name="random")
]
