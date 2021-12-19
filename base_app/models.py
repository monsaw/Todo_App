from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE , blank = True, null = True)
    title = models.CharField(max_length=200)
    description = models.TextField( blank= True , null = False)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(default = timezone.now())

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete'] 