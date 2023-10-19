from django.urls import path
from ServerWeb import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('form_beacon/', views.form_beacon, name='form_beacon'),
    path('form_artwork/', views.form_artwork, name='form_artwork'),
    path('logout/', views.sign_out, name='logout'),
]
