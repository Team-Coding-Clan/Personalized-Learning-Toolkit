from django.db import models


# Create your models here.

# using default Django User model

# class registeration(models.Model):  # api_registration
#     username = models.CharField(max_length=50, name="username")
#     email = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     confirmpassword = models.CharField(max_length=100, default=" ")
#
#     class Meta:
#         db_table = "userdata"


class connect(models.Model):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('T', 'Transgender'),
        ('O', 'Other'),
    )
    fname = models.CharField(max_length=100, default=None, primary_key=True)
    lname = models.CharField(max_length=100, default=None)
    linkedin = models.CharField(max_length=100, default=None)
    github = models.CharField(max_length=100, default=None)
    hackerrank = models.CharField(max_length=100, default=None)
    myways = models.CharField(max_length=100, default=None)
    skillknown = models.CharField(max_length=50, default=None)
    skilllearn = models.CharField(max_length=50, default=None)
    gender = models.CharField(max_length=30, default=None, choices=GENDER)

    class Meta:
        db_table = "profiles"