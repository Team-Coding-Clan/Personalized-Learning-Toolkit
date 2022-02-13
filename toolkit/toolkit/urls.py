from django.contrib import admin
from django.urls import path
from apis import views

# from connect.views import userConnect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('connect/', views.userConnect, name="profile"),
    path('login/', views.login),
    path('home/', views.home),
    path('recommendation/', views.recommend, name="recommendation"),
    path('external/', views.external),
]
