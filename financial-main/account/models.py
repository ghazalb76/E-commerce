from django.db import models


class Account(models.Model):
    user_id = models.IntegerField()
    balance = models.IntegerField(default=1000)

