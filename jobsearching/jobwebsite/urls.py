from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('profile/', views.profile),
    path('support/', views.support),
    path('findJob/', views.findJob)

]
