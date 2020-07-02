from django.urls import path, include
from . import views
from .api import RegistrationAPI, LoginAPI, UserAPI
from knox import views as knox_views

urlpatterns = [
    #path("api/users/", views.ProfileListCreate.as_view()),
    path('auth', include('knox.urls')),
    path('auth/register', RegistrationAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/user', UserAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view(), name = 'knox_logout') #clears the token, so users have to log back in
]

#Register, Login, Logout post requests
#User get request