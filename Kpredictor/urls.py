from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
import Account.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',Account.views.welcome,name="home"),
    path('account/', include('Account.urls')),
    path('news/', include('news.urls')),
    path('predictor/', include('predictor.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)