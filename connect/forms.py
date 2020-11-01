from django import forms
from connect.models import connect


class Connect(forms.ModelForm):
    class Meta:
        model = connect
        fields = "__all__"
