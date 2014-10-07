from django.conf.urls.defaults import *
from dbe.photo.models import *

urlpatterns = patterns('dbe.photo.views',
   (r"^(\d+)/$", "album"),
   (r"^(\d+)/(full|thumbnails|edit)/$", "album"),
   (r"^update/$", "update"),
   (r"^search/$", "search"),
   (r"^image/(\d+)/$", "image"),
   (r"", "main"),
)
