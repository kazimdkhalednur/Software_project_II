from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("signup/", views.SignUpView.as_view()),
    path("login/", views.ObtainAuthToken.as_view()),
    path("info/", views.UserInfoView.as_view()),
    path("change-password/", views.ChangePasswordAPIView.as_view()),
]
