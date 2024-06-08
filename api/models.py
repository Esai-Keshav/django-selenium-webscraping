from django.db import models
# from main import collect
# Create your models here.

class Data(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
