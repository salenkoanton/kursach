from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"^(\d+)/wall", views.wall, name = "wall"),

]