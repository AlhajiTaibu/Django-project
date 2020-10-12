from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Expense(models.Model):
    amount = models.FloatField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    description = models.TextField()
    date = models.DateField(default=now)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
