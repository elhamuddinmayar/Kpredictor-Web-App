from django.urls import path
from django.contrib.auth import views as auth_views
from .import views


urlpatterns = [
    path('second/', views.second, name='second'),
    path("register/",views.register,name="register"),
    path("login/", views.login_view, name="login"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

   
