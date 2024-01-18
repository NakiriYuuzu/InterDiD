from django.urls import path
from ServerApi.line.linebot import LinebotView
from ServerApi.views import *
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView

urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/verify', TokenVerifyView.as_view()),

    path('linebot', LinebotView.as_view()),

    path('user', UsersView.as_view()),
    path('account', AccountsView.as_view()),
    path('beacons', BeaconsView.as_view()),
    path('artworks', ArtworksView.as_view()),
]
