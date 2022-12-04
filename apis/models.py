from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# using default Django User model

class connect(models.Model):
    linkedin = models.URLField(default = None)
    github = models.CharField(max_length = 500, default = None)
    known_skills = models.JSONField(null = True)
    skills_to_learn = models.CharField(max_length = 50, default = None)
    user_id = models.OneToOneField(User, on_delete = models.CASCADE)

    class Meta:
        db_table = "connect"


# list of JSON
class Resources(models.Model):
    skill = models.CharField(max_length = 500)
    youtube = models.JSONField()
    google_books = models.JSONField()
    count = models.IntegerField(default = 1)

    class Meta:
        db_table = "resources"
