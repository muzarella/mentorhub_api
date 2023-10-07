# multi_vendor/urls.py
from django.urls import path
from .views import vendor_home, MembersProfile

urlpatterns = [
    # -----ORGANIZATIONS URL--------------------
    path('organizations/<str:unique_id>/', vendor_home, name='vendor_home'),


    # -----MEMBERS (mentees and mentors) URLS-------------
    path('membersDashboard/', MembersProfile.as_view(), name='membersDashboard'),
]
