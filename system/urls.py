from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from django.conf import settings
from django.conf.urls.static import static


def homepage(request):
    return render(request, 'system/base.html')


urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('course/', include('course_valute.urls')),
    path('food/', include('food_site.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
