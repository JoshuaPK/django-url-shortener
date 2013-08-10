from django.db import models
from django.conf import settings

from shortener.baseconv import base62


class Link(models.Model):
    """
    Model that represents a shortened URL
    """
    url = models.URLField(max_length=2048)
    date_submitted = models.DateTimeField(auto_now_add=True)
    usage_count = models.PositiveIntegerField(default=0)

    def to_base62(self):
        return base62.from_decimal(self.id)

    def __unicode__(self):
        return  '%s : %s' % (self.to_base62(), self.url)

    class Meta:
        get_latest_by = 'date_submitted'

class Referrer(models.Model):
    """
    Model that represents an instance of a click on a shortened link.
    """
    url = models.ForeignKey(Link)
    date_clicked = models.DateTimeField(auto_now_add=True)
    referrer = models.URLField(max_length=2048)
    who_ip_clicked = models.IPAddressField()

class TagList(models.Model):
    """
    Model that represents the tags themselves.
    """
    tag_text = models.CharField(max_length = 64)
    tag_desc = models.TextField()
    number_of_times_used = models.BigIntegerField()
    

class URLTags(models.Model):
    """
    Model that represents the tags attached to each URL.
    """
    url = models.ForeignKey(Link.id)
    date_added = models.DateTimeField(auto_now_add=True)
    who_added = models.User
    who_ip_added = models.IPAddressField()
    tag_text = models.ManyToManyField(TagList)
