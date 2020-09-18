from django.db import models
from django.urls import reverse

# Create your models here.
class Employee (models.Model):
    name = models.CharField (max_length = 100)
    point = models.FloatField()
    phone = models.CharField(max_length = 10)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('update_employee', kwargs={'id':self.id})

   