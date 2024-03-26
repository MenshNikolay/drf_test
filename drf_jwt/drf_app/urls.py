from django.urls import path
from .views import ReferralCodeCreateView, ReferralCodeDeleteView

urlpatterns = [
    path('referral/code/create/', ReferralCodeCreateView.as_view(), name='referral_code_create'),
    path('referral/code/delete/', ReferralCodeDeleteView.as_view(), name='referral_code_delete'),
]