
from django.db import models
from django.utils.timezone import now
from django.core.cache import cache
from django.contrib.auth.models import User




class Topic(models.Model):
    user = models.ForeignKey(User)
    photo = models.ImageField(upload_to="photo")
    wid = models.IntegerField(default=0, blank=True)
    name = models.CharField(max_length=16,default="", blank=True)
    public = models.BooleanField(default=False)
    polls = models.PositiveIntegerField(default=0)
    ctime = models.DateTimeField(default=now)

    def ranking(self):
        return Topic.objects.filter(polls__gt=self.polls).count() + 1


class Poll(models.Model):
    user = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)

