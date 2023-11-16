from django.conf.urls.static import static
from django.urls import path

from InterDiD import settings
from ServerWeb import views

urlpatterns = [
    # LANDING PAGE
    path('', views.index, name='index'),

    # ADMIN
    path('admin/', views.dashboard, name='index'),
    path('admin/login/', views.sign_in, name='login'),
    path('admin/form_beacon/', views.form_beacon, name='form_beacon'),
    path('admin/list_artwork/', views.list_artwork, name='list_artwork'),
    path('admin/form_artwork/', views.form_artwork, name='form_artwork'),
    path('admin/logout/', views.sign_out, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
