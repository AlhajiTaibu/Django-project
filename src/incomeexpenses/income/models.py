from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Income(models.Model):
    amount = models.FloatField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    description = models.TextField()
    date = models.DateField(default=now)
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ['-date']


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

