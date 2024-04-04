from django.urls import path, include
from django.contrib import admin
from drf_app.views import RegisterView, RefCodeInitView, RefCodeInitView, ReferralListView, RegesterViaRefCode
from .yasg import urlpatterns as doc_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf_app/', include('drf_app.urls')),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/referral-code/create/', RefCodeInitView.as_view(), name='referral-code-create'),
    path('api/referral-code/delete/', RefCodeInitView.as_view(), name='referral-code-delete'),
    path('api/register-via-code/', RegesterViaRefCode.as_view(), name='register-referral-user'),
    path('api/referrals/<int:referrer_id>/', ReferralListView.as_view(), name='referral-list'),



]



urlpatterns += doc_url