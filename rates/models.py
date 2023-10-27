from django.db import models


class Rate(models.Model):
    days = models.TextField()
    times = models.TextField()
    tz = models.TextField()
    price = models.IntegerField()
