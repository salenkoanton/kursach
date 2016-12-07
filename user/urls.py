from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"^login/", views.Login.as_view(), name = "login"),
    url(r"^logout/$", views.Logout.as_view(), name = "logout"),
    url(r"^auth$", views.auth, name = "authorisation"),
    url(r"^users$", views.users, name = "users"),
    url(r"^(\d+)$", views.Users_id.as_view(), name="users_id"),
    url(r"^(\d+)/wall$", views.Users_id_wall.as_view(), name='wall'),
    url(r"^(\d+)/followers$", views.Users_id_followers.as_view(), name='followers'),
    url(r'^author/(\d+)', views.Author_id.as_view(), name = 'author'),
    url(r'^authors/$', views.authors, name = 'authors'),
    url(r'^search$', views.search, name='search'),
    url(r'^$', views.main, name='main'),
]
