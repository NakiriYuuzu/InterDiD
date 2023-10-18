from django.urls import path
from ServerApi.line.linebot import LinebotView

urlpatterns = [
    path('linebot', LinebotView.as_view())
]
