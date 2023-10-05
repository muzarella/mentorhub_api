from django.urls import path

from .views import MembersProfile

urlpatterns = [
    path('dashboard/', MembersProfile.as_view(), name='member_dashboard'),
]