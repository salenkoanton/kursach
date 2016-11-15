from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"^login", views.Login.as_view(), name = "login"),
    url(r"^auth", views.auth, name = "authorisation"),
    url(r"^users$", views.users, name = "users"),
    url(r"^(\d+)$", views.Users_id.as_view(), name="users_id"),
    url(r"^(\d+)/wall$", views.Users_id_wall.as_view(), name='wall'),
    url(r"^(\d+)/followers$", views.Users_id_followers.as_view(), name='followers'),
]
