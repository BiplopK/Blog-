from django.urls import path
from .views import *

urlpatterns = [
    path("register/",UserRegistrationView.as_view(),name='register'),
    path("login/",LoginView.as_view(),name='login'),
    path("logout/",LogoutView.as_view(),name='logout'),
]
