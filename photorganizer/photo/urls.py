from django.conf.urls import patterns, include, url
from photo import views

urlpatterns = patterns('',
    url(r'^$', views.main, name='main'),
    url(r"^(\d+)/(full|thumbnails|edit)/$", views.album, name='album'),
    url(r"^image/(\d+)/$", views.image, name="image"),
    url(r"^update/$", views.update, name="update"),
    url(r"^search/$", views.search, name="search"),
)
