from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """ Модель пользователя """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    friends = models.ManyToManyField(to=User, related_name="friends", blank=True)
    first_name = models.CharField(verbose_name="First name", max_length=24, blank=True)
    last_name = models.CharField(verbose_name="Last name", max_length=24, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}"
