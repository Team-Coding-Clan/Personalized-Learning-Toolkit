from django.contrib import admin
from django.urls import path
from getData import views
from connect.views import userConnect
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('connect/', userConnect, name="profile"),
    path('login/',views.login),
    path('home/',views.home),
    path('recommendation/',views.recommend, name="recommendation"),
    url(r'external/', views.external),
]
