from django.contrib import admin
from django.urls import include, path
from Account import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Account.urls')),
    path('home/',views.welcome,name="home"),
]
