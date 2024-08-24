
from django.db import models
from django import forms
from django.contrib.auth.models import User


# Create your models here.
class Housing(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=500)
    rent = models.IntegerField()
    location = models.CharField(max_length=500)
    footage = models.CharField(max_length=500 , default="")
    bed = models.CharField(max_length=500)
    bath = models.CharField(max_length=500)
    description = models.CharField(max_length=100000, default="")
    link = models.CharField(max_length=10000, default="")
    imgadd = models.CharField(max_length=10000, default="")
    popularity = models.IntegerField(default=0)
    num_surveys = models.IntegerField(default=0)
    average_rating = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    num_ratings= models.IntegerField(default=0)
    favorites = models.ManyToManyField(
        User, related_name='favorite', default=None, blank=True
    )
    official = models.BooleanField(default=False)

    def __str__(self):
        return self.title
