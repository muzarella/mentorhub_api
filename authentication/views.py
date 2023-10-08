
from django.http import HttpResponsePermanentRedirect
import os
from django.shortcuts import render, redirect
from rest_framework import generics, status, views, permissions
from .serializers import RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, EmailVerificationSerializer, LoginSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.template.loader import render_to_string
# Import ObjectDoesNotExist exception
from django.core.exceptions import ObjectDoesNotExist
from jwt.exceptions import InvalidAlgorithmError

# -------------------------------REGISTER---------------------------


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)  # Make sure to define UserRenderer

    def post(self, request, org_id):
        user_data = request.data
        user_data['AffiliatedOrg'] = org_id  # Save org_id as unique_id
        print(org_id)
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + \
            relativeLink + "?token=" + str(token)

        context = {'user': user, 'absurl': absurl}
        email_body = render_to_string('mail.html', context)

        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email to Activate your Account'}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)
# -------------------------------END OF REGISTER---------------------------


# -------------------------------VERIFY EMAIL ADDRESS---------------------------
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    # to enable us test through swagger
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidAlgorithmError:
            return Response({'error': 'Invalid token algorithm'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        # -------------------------------END VERIFY EMAIL ADDRESS---------------------------


# -------------------------------LOGIN---------------------------
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in Successfully',
            'data': serializer.data,
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)
# -------------------------------LOGIN---------------------------


# -------------------------------SEND CHANGE PASSWORD LINK TO CHANGE PASSWORD--------------------------
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        try:
            # Try to retrieve the user with the provided email
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            absurl = 'http://'+current_site + relativeLink

            # Create a dictionary to pass context data to the template
            context = {'user': user, 'absurl': absurl}

            # Render the HTML template
            email_body = render_to_string('resetpasswordemail.html', context)

            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}

            Util.send_email(data)

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
# -------------------------------END OF SEND CHANGE PASSWORD LINK TO CHANGE PASSWORD---------------------------


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


# --------CHECK TOKEN IF VALID TO CHANGE PASSWORD------------------
class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url', '')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return self.invalid_token_response(redirect_url)

            # If the token is valid, proceed with your logic here
            return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)

        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            return self.invalid_token_response(redirect_url)

    def invalid_token_response(self, redirect_url):
        if redirect_url:
            # Append query parameters to the redirect URL
            redirect_url += '?token_valid=False'
        else:
            redirect_url = os.environ.get(
                'FRONTEND_URL', '') + '?token_valid=False'

        return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
# --------END OF CHECK TOKEN IF VALID TO CHANGE PASSWORD------------------


# ---------------------------UPDATE PASSWORD-----------------------
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password was changed successfully'}, status=status.HTTP_200_OK)
# ---------------------------END UPDATE PASSWORD-----------------------


# ---------------------------LOGOUT-----------------------
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
# ---------------------------END OF LOGOUT-----------------------
