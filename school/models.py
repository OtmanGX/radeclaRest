from django.db import models


class School(models.Model):
    name = models.CharField(max_length=50, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    responsible = models.CharField(max_length=35, blank=True)
    trainers = models.TextField(blank=True)
