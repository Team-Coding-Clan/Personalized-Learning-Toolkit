from django.contrib import admin
from django.urls import path
from apis import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # user
    path('register/', views.RegisterView.as_view(), name = 'auth_register'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # refresh access token using refresh token
    path('login/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),

    # for generating tokens
    path('login/', views.MyObtainTokenPairView.as_view(), name = 'token_obtain_pair'),
    path('logout_token/', views.APILogoutView.as_view(), name = 'logout_token'),

    # get additional information
    path('users/', views.ListUsers.as_view(), name = "profile"),
    path('profile/', views.ProfileView.as_view(), name = "profile"),
    path('connect/', views.CreateConnectView.as_view(), name = "profile"),

    # update profile
    path('update_profile/<int:user_id_id>/', views.UpdateConnectView.as_view(), name = 'update_profile'),
    path('home/', views.home, name = 'homepage'),

    # recommendations
    path('recommendations/', views.get_recommendations, name = "recommendations"),
    # todo: change endpoint to include user id

    path("feedback/", views.FeedbackFormView.as_view(), name = "feedback"),
    path("success/", views.SuccessView.as_view(), name = "success"),

    path("personalized_recommendations/", views.personalised_recommendations, name = "personalised_recommendations"),
    path("general_recommendations/", views.general_recommendations, name = "general_recommendations")
]
