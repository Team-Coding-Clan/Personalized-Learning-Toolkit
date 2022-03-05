from django import forms
from apis.models import connect
from django import forms
from django.contrib.auth.models import User


class Register(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class Login(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ("username", "password")


class Connect(forms.ModelForm):
    class Meta:
        model = connect
        fields = "__all__"

