from django import forms
from apis.models import connect
from django import forms
from django.contrib.auth.models import User


class Register(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class Login(forms.Form):
    username = forms.CharField(max_length = 100)
    password = forms.CharField(max_length = 250)

    class Meta:
        model = User
        fields = ("username", "password")


class Connect(forms.ModelForm):
    class Meta:
        model = connect
        fields = "__all__"


# Removed: from time import sleep
# Removed: from django.core.mail import send_mail
from django import forms
from apis.tasks import send_feedback_email_task


class FeedbackForm(forms.Form):
    email = forms.EmailField(label = "Email Address")
    message = forms.CharField(
        label = "Message", widget = forms.Textarea(attrs = {"rows": 5})
    )

    def send_email(self):
        send_feedback_email_task.delay(
            self.cleaned_data["email"], self.cleaned_data["message"]
        )
