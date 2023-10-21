from django.urls import path
from ServerWeb import views

urlpatterns = [
    # LANDING PAGE

    # ADMIN
    path('admin/', views.index, name='index'),
    path('admin/login/', views.sign_in, name='login'),
    path('admin/form_beacon/', views.form_beacon, name='form_beacon'),
    path('admin/form_artwork/', views.form_artwork, name='form_artwork'),
    path('admin/logout/', views.sign_out, name='logout'),
]
