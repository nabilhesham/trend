from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trend/', include('trend_app.urls')),
    path('api/', include('trend_app.api.urls')),
]
