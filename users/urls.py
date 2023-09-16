from django.urls import path
from . import views

urlpatterns = [
    path('api-token/', views.CustomAuthToken.as_view()),
]
