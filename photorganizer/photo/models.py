# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from string import join
import os
from PIL import Image as PImage
from django.core.files import File
from os.path import join as pjoin
from tempfile import NamedTemporaryFile
from django.utils.encoding import smart_str
#from .settings import MEDIA_ROOT

#что --то не получается импортировать медиа рут
MEDIA_ROOT='/home/vados/django/photorganizer/photorganizer/media'

class Album(models.Model):
    title = models.CharField(max_length=60)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def images(self):
        lst = [x.image.name for x in self.image_set.all()]
        lst = ["<a href='/media/%s'>%s</a>" % (x, x.split('/')[-1]) for x in lst]
        return join(lst, ', ')
    images.allow_tags = True

class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __unicode__(self):
        return self.tag


class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to="images/")
    tags = models.ManyToManyField(Tag, blank=True)
    albums = models.ManyToManyField(Album, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=50)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True)
    thumbnail2 = models.ImageField(upload_to="images/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="images/", blank=True, null=True)



    def __unicode__(self):
        return self.image.name


    def save(self, *args, **kwargs):
        """Save image dimensions."""
        super(Image, self).save(*args, **kwargs)
        im = PImage.open(pjoin(MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size

        # large thumbnail
        fn, ext = os.path.splitext(self.image.name)
        im.thumbnail((128,128), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb2" + ext
        tf2 = NamedTemporaryFile()
        im.save(tf2.name, "JPEG")
        self.thumbnail2.save(thumb_fn, File(open(tf2.name)), save=False)
        tf2.close()

        # small thumbnail
        im.thumbnail((40,40), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb" + ext
        tf = NamedTemporaryFile()
        im.save(tf.name, "JPEG")
        self.thumbnail.save(thumb_fn, File(open(tf.name)), save=False)
        tf.close()

        super(Image, self).save(*args, ** kwargs)

    def size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)


    def tags_(self):
        lst = [x[1] for x in self.tags.values_list()]
        #UnicodeEncodeError 'ascii' codec can't encode characters in position
        #see https://www.evernote.com/shard/s118/sh/b2b30f5a-7523-43c9-8b18-393fabbc3180/3d924a0b8dbbc1d1df2e221db7417317
        #return str(join(lst, ', '))
        return smart_str(join(lst, ', '))

    def albums_(self):
        lst = [x[1] for x in self.albums.values_list()]
        return smart_str(join(lst, ', '))

    #def thumbnail_(self):
    #    return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" /></a>""" % (
    #                                                    (self.image.name, self.thumbnail.name))
    #thumbnail.allow_tags = True
