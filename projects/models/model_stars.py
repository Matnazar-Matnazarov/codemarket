from django.db import models
from accounts.models.accounts import CustomUser


class Stars(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.stars}"
