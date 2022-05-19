
from django.db import models

from users.models import Profile

class Book(models.Model):
    title = models.CharField(max_length=140)
    author = models.CharField(max_length=140)
    users = models.ManyToManyField(to=Profile, verbose_name="Пользователи", related_name="books", blank=True)
    year = models.IntegerField()
    finished = models.BooleanField()
    
    def __str__(self):
        return f"{self.title} | {self.author}"