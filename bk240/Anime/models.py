from django.db import models

MAX_TITLE_LENGTH = 128


class Anime(models.Model):
    aid = models.CharField(max_length=16)
    mainTitle = models.CharField(max_length=MAX_TITLE_LENGTH)
    jaTitle = models.CharField(max_length=MAX_TITLE_LENGTH)
    zhTitle = models.CharField(max_length=MAX_TITLE_LENGTH)
    # Movie TV OVA Web Special Other
    aniType = models.CharField(max_length=64)
    episodeCnt = models.IntegerField()
    airDate = models.DateField()
    endDate = models.DateField()
