from django.urls import path
from api.auth import views

app_name = 'api_auth'

urlpatterns = [
    path("login/", views.LoginView.as_view(), name='login'),
    path("refresh/", views.RefreshTokenView.as_view(), name='refresh'),
    path("verify/", views.VerifyTokenView.as_view(), name='verify'),
]