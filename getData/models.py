from django.db import models

# Create your models here.

class registeration(models.Model):
    username = models.CharField(max_length=50, name="username")
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirmpassword = models.CharField(max_length=100, default=" ")

    class Meta:
        db_table = "userdata"
