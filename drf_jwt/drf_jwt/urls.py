from django.urls import path, include
from django.contrib import admin
from drf_app.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf_app/', include('drf_app.urls')),
    path('api/register/', RegisterView.as_view(), name='register'),
]
