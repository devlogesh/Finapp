from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',UserSignup.as_view() , name='user_create'),
    
]