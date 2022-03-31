from django.contrib import admin
from django.urls import path
from apis import views
from rest_framework_simplejwt.views import TokenRefreshView

# from connect.views import userConnect


urlpatterns = [
    path('admin/', admin.site.urls),

    # user
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # refresh access token using refresh token
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # for generating tokens
    path('login/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('logout_token/', views.APILogoutView.as_view(), name='logout_token'),

    # get additional information
    path('connect/', views.ConnectView.as_view(), name="profile"),
    path('update/<int:pk>/', views.ProfileUpdate.as_view(), name="update"),

    # path('login/', views.login),
    path('home/', views.home, name='homepage'),
    path('recommendation/', views.recommend, name="recommendation"),
    path('external/', views.external),

]
