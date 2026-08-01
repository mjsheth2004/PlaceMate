from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    STUDENT = "STUDENT"
    COMPANY = "COMPANY"
    PLACEMENT_OFFICER = "PLACEMENT_OFFICER"

    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (COMPANY, "Company"),
        (PLACEMENT_OFFICER, "Placement Officer"),
    ]

    role = models.CharField(
        max_length=25,
        choices=ROLE_CHOICES,
        default=STUDENT
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    profile_photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username