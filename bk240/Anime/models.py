from django.db import models

MAX_TITLE_LENGTH = 128
MAX_USER_NAME_LENGTH = 128


class Anime(models.Model):
    aid = models.CharField(max_length=16)
    mainTitle = models.CharField(max_length=MAX_TITLE_LENGTH)
    jaTitle = models.CharField(max_length=MAX_TITLE_LENGTH, null=True)
    zhTitle = models.CharField(max_length=MAX_TITLE_LENGTH, null=True)
    # Movie TV OVA Web Special Adult Other
    aniType = models.CharField(max_length=64, null=True)
    episodeCnt = models.IntegerField(null=True)
    airDate = models.DateField(null=True)
    endDate = models.DateField(null=True)


class User(models.Model):
    userName = models.CharField(max_length=MAX_USER_NAME_LENGTH)
    password = models.CharField(max_length=256)
    privilege = models.IntegerField()
    mail = models.CharField(max_length=MAX_USER_NAME_LENGTH)
