from django.db import models


# Create your models here.

# using default Django User model

class connect(models.Model):
    linkedin = models.CharField(max_length=100, default=None)
    github = models.CharField(max_length=100, default=None)
    known_skills = models.CharField(max_length=50, default=None)
    skills_to_learn = models.CharField(max_length=50, default=None)

    class Meta:
        db_table = "profiles"
