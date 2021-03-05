from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "home"),
    # path("", views.ajax_post_search, name = "app")
]