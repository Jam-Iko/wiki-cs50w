from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.search, name="search-results-view"),
    path("wiki/create", views.create, name="create-entry-view"),
    path("wiki/random", views.random_entry, name="random-entry-view"),
    path("wiki/<str:title>/edit", views.edit, name="edit-entry-view"),
    path("wiki/<str:title>", views.entry, name="entry-view")
]
