from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('api/logout', views.log_out, name="logout"),
    path('inventory/', views.inventory, name='inventory'),
    path('register/', views.register, name="register"),
    path('createitem/', views.create_item, name="createitem")
]