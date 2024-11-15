from django.urls import path

from . import views
# app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),

    path("create", views.create, name="create"),
    path("random", views.random_page, name="random"),
    path("<str:title_name>/edit", views.edit, name="edit"),
    path("<str:title_name>", views.title, name="title"),

]
