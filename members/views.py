from django.shortcuts import render, redirect,  get_object_or_404
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect
import os

from .permissions import IsMemberOrOrganization
from .serializers import MembersSerializer
from .models import Member


# -----------Members Profile -|Dashboard------------------
class MembersProfile(generics.RetrieveAPIView):
    serializer_class = MembersSerializer
    permission_classes = (permissions.IsAuthenticated, IsMemberOrOrganization,)

    def get(self, request):
        member = get_object_or_404(Member, user=request.user)
        data = MembersSerializer(member).data
        return Response(data, status=status.HTTP_200_OK)
