from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"^", views.Playlist.as_view(), name = "playlist"),

]