from django.contrib import admin
from .models import Album, Image, Tag

# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title"]

class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", "albums_", "title", "user", "rating", "size", "tags_",  "thumbnail", "thumbnail2", "created" ]
    list_filter = ["tags", "albums", "user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
