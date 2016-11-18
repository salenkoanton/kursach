from django.conf.urls import url
from . import api_views
urlpatterns = [
    url(r"^blog/(\d+)/wall", api_views.Wall.as_view(), name = "Wall"),
    url(r"^audio/$", api_views.Playlist.as_view(), name="playlist"),
    url(r"^audio/(\d+)", api_views.Audios_id.as_view(), name="user_audio"),
    url(r"^login/", api_views.Login.as_view(), name="login"),
    url(r"^logout/$", api_views.Logout.as_view(), name="logout"),
    url(r"^auth$", api_views.auth, name="authorisation"),
    url(r"^users$", api_views.users, name="users"),
    url(r"^(\d+)$", api_views.Users_id.as_view(), name="users_id"),
    url(r"^(\d+)/wall$", api_views.Users_id_wall.as_view(), name='wall'),
    url(r"^(\d+)/followers$", api_views.Users_id_followers.as_view(), name='followers'),
    url(r'^author/(\d+)', api_views.author, name='author'),
    url(r'^authors/$', api_views.authors, name='authors'),
    url(r'^blog/following/$', api_views.following, name='following'),

]
