from django.shortcuts import render, redirect, get_object_or_404
from .forms import Register, Login
from django.db import connection
import sys
from subprocess import run, PIPE
from .forms import connect

from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ConnectSerializer
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST


# login
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

# def userConnect(request):
#     if request.method == "POST":
#         form = connect(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return render(request, "userConnect.html", {"msg": "Connected."})
#                 # return Response({'status': 'Success'}, status=HTTP_200_OK)
#             except:
#                 print("pass")
#                 pass
#     else:
#         form = connect()
#         print("Not connected.")
#     return Response({'status': 'Success'}, status=HTTP_400_BAD_REQUEST)

class ConnectView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConnectSerializer

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     # update the instance
    #     instance.linkedin = request.data.get('linkedin', instance.linkedin)
    #     instance.github = request.data.get('github', instance.github)
    #     instance.known_skills = request.data.get('known_skills', instance.known_skills)
    #     instance.skills_to_learn = request.data.get('skills_to_learn', instance.skills_to_learn)
    #     instance.save()
    #
    #     serializer = self.get_serializer(instance)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     return Response(serializer.data)


class ProfileUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConnectSerializer
    queryset = connect.objects.all()
