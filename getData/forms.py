from django import forms
from getData.models import registeration


class Register(forms.ModelForm):
    class Meta:
        model = registeration
        fields = "__all__"

class Login(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=250)

    class Meta:
        model = registeration
        fields = ("username","password")
