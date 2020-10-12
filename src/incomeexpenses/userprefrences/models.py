from django.conf import settings
from django.db import models


class UserPreferences(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    currency = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.user}s preferences'
