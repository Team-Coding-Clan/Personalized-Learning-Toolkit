from django.shortcuts import render
from .forms import connect, FeedbackForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer, ProfileSerializer, \
    ConnectSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User
from rest_framework import generics, status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser

from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
                                   HTTP_409_CONFLICT, HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)

from .helpers import youtube_api, google_books_api
from .models import Resources


# login
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# register
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
            for token in OutstandingToken.objects.filter(user = request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token = token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token = refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})


# homepage
def home(request):
    return render(request, "homepage.html")


# recommendations : depricated
# def recommend(request):
#     return render(request, "recommendation.html")


class CreateConnectView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConnectSerializer

    # todo : serializer also has create and update
    # def post(self, request, format=None):
    #     serializer = ConnectSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateConnectView(generics.UpdateAPIView):
    queryset = connect.objects.all()
    serializer_class = ConnectSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'user_id_id'


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires authentication.
    """
    permission_classes = (IsSuperUser,)

    def get(self, request, format = None):
        """
        Return particular user
        """
        data = User.objects.all()
        serializer_data = UserSerializer(data = data, many = True)
        serializer_data.is_valid()
        return Response(serializer_data.data)


class ProfileView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format = None):
        """
        Return particular user
        """
        data = connect.objects.filter(user_id_id = request.user.pk)
        serializer_data = ProfileSerializer(data = data, many = True)
        serializer_data.is_valid()
        return Response(serializer_data.data)


# will be a scheduler function
@csrf_protect
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_recommendations(request):
    if request.method == 'GET':
        # try:
        if not connect.objects.filter(user_id_id = request.user.id).exists():
            return JsonResponse({'Status': 'Create a User profile first'})
        user_profile = connect.objects.get(user_id_id = request.user.id)
        skills_to_learn = user_profile.skills_to_learn  # returns csvs
        skills_to_learn = list(map(str.strip, skills_to_learn.split(',')))
        known_skills = user_profile.known_skills  # returns a python list
        search_keys = skills_to_learn + known_skills

        if not search_keys:
            return JsonResponse({'Status': 'No skills to learn'}, status = HTTP_200_OK)

        # already skill exists in database
        existing_skills = Resources.objects.values_list('skill', flat = True)
        # remove from search_keys
        # print(search_keys)

        # the below line is commented as I have added count to the table of recommendations
        # that means every skill counts :)
        # search_keys = set(search_keys) - set(existing_skills)

        # print(existing_skills)
        # print(search_keys)
        # add into the database
        for skill in search_keys:
            if Resources.objects.filter(skill = skill).exists():
                count = Resources.objects.get(skill = skill).count
                Resources.objects.filter(skill = skill).update(count = count + 1)
            else:
                resource = Resources(skill = skill, youtube = youtube_api(skill),
                                     google_books = google_books_api(skill))
                resource.save()
        return JsonResponse({'Status': 'True'}, status = HTTP_200_OK, safe = False)
        # call the APIs, this will go into the Task Scheduler
        # except Exception as e:
        #     return JsonResponse({'Status': 'Error Occurred'}, status = HTTP_400_BAD_REQUEST, safe = False)


class FeedbackFormView(FormView):
    template_name = "feedback/feedback.html"
    form_class = FeedbackForm
    success_url = "/success/"

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class SuccessView(TemplateView):
    template_name = "feedback/success.html"


@csrf_protect
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def general_recommendations(request):
    """
    endpoint for general skill recommendation for homepage
    """
    # Reserved.objects.filter(client=client_id).order_by('-check_in')
    # get most common 5 skills for general recommendations
    recommendations = []
    entries = Resources.objects.all().order_by('-count')[:5]
    for entry in entries:
        recomm = {}
        recomm[entry.skill] = [entry.youtube[0], entry.youtube[1], entry.google_books[0]]
        recommendations.append(recomm)
    return Response(recommendations, status = HTTP_200_OK)


@csrf_protect
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def personalised_recommendations(request):
    """
    endpoint for personalised skill recommendations
    ordered by skill
    """

    # get the already known skills
    # and the new skills
    known_skills = connect.objects.get(user_id_id = request.user.id).known_skills
    new_skills = connect.objects.get(user_id_id = request.user.id).skills_to_learn
    new_skills = list(map(str.strip, new_skills.split(',')))

    # print(type(known_skills))
    # print(type(new_skills))
    skills = known_skills + new_skills
    # get the recommendations
    # 2 for youtube of each skill
    # 1 book recommendation
    # these have to be arranged by languages
    recommendations = []

    for skill in skills:
        recomm = {}
        data = Resources.objects.filter(skill = skill).values()
        recomm[skill] = [data[0]['youtube'][0], data[0]['youtube'][1], data[0]['google_books'][0]]
        recommendations.append(recomm)
    # print(data[0]['youtube'][0])
    # print(data[0]['youtube'][1])
    # print(data[0]['google_books'][0])
    # print(recommendations)
    return Response(recommendations, status = HTTP_200_OK)
