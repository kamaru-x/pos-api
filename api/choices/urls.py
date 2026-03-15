from django.urls import path

from api.choices import views

app_name = 'api_choices'

urlpatterns = [
    path("all", views.ChoicesAPIView.as_view(), name="choices"),
]