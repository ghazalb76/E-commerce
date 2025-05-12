from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
