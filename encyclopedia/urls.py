from django.urls import path

from . import views

#ROOT_URLCONF = 'wiki.urls'

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name = "search"),
    path("randoms", views.randoms, name="randoms"),
    path("create", views.create, name = "create"),
    path('<str:title>/edit', views.edit, name ='edit'),
    path("<str:title>", views.entry, name="entry"),
]
