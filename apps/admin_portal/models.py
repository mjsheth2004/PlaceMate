from django.db import models
from django.conf import settings

class OfficerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.full_name or self.user.email
