from django.conf.urls import url
from . import views
urlpatterns = [
    url("^login", views.login, name = "login"),
    url("^auth", views.auth, name = "authorisation"),
    url("^users$", views.users, name = "users"),
    url("^(\d+)$", views.Users_id.as_view(), name="users_id"),
    url("^(\d+)/wall$", views.Users_id_wall.as_view(), name='wall'),
    url("^(\d+)/followers$", views.Users_id_followers.as_view(), name='followers'),
]