from django.db import models

class Game(models.Model):
    secret_number = models.CharField(max_length=3)
    guesses = models.IntegerField(default=0)
