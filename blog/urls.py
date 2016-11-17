from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"^(\d+)/wall", views.Wall.as_view(), name = "Wall"),
    url(r"^(\d+)/followers", views.followers, name = 'followers'),
]