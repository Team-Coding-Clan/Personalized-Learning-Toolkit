from django.shortcuts import render
from .forms import Register, Login
from django.db import connection
import sys
from subprocess import run, PIPE
from .forms import Connect

from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# logout
class APILogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})


def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request, "register.html", {"msg": "Successfully registered\nWelcome!."})
                # return render()
            except:
                print("pass")
                pass
        else:
            form = Register
            print("Registeration unsuccessful")
    return render(request, "register.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        cursor = connection.cursor()
        p = cursor.execute(
            "Select * from mydatabase.userdata where username = '" + username + "' and password = '" + password + "'")
        print(p)
        data = cursor.fetchone()
        print(data)
        if (data is None):
            return render(request, 'login.html', {'context': 'Not a user !'})
        else:
            return render(request, 'homepage.html')
    else:
        form = Login()
    return render(request, "login.html", {"form": form})


def home(request):
    return render(request, "homepage.html")


def external(request):
    # input1 = request.POST.get("parameter1")
    # input2 = request.POST.get("parameter2")
    # /home/tawishi/Desktop/projects/pythonScripts/dataset1.py
    output = run([sys.executable, r'/home/tawishi/Desktop/projects/pythonScripts/dataset1.py'], shell=False,
                 stdout=PIPE)
    print(output)

    return render(request, "recommendation.html", {'data': output.stdout.strip().decode("utf-8")})


def recommend(request):
    return render(request, "recommendation.html")


# Create your views here.

def userConnect(request):
    if request.method == "POST":
        form = Connect(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request, "userConnect.html", {"msg": "Connected."})
            except:
                pass
    else:
        form = Connect()
        print("Not connected.")
    return render(request, "userConnect.html", {"form": form})
