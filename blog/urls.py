from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"^$", views.main, name = "main"),
    url("^bla", views.bla, name = "bla"),
    url("^passport", views.passport, name = "pasport"),
    url("^prods/(\d+)/$", views.prods_id.as_view(), name="prods_id"),
    url("^prods$", views.prods, name = "prods"),


]