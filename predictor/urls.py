from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('input/', views.input_view, name='input'),
    path('predict/', views.predict, name='predict')
]
