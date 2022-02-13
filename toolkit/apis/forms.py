from django import forms
from apis.models import registeration, connect
from django import forms


class Register(forms.ModelForm):
    class Meta:
        model = registeration
        fields = "__all__"


class Login(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=250)

    class Meta:
        model = registeration
        fields = ("username", "password")


class Connect(forms.ModelForm):
    class Meta:
        model = connect
        fields = "__all__"

