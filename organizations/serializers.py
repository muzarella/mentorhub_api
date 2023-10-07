from organizations.exceptions import CustomException
from authentication.models import User
from rest_framework import serializers, generics, status
from rest_framework.response import Response
from .models import Member
from authentication.serializers import RegisterSerializer


class MembersSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()

    class Meta:
        model = Member
        fields = ['user', 'MentoringRole', 'profile_picture', 'country', 'state', 'phone_number',
                  'Timezone', 'LinkedIn', 'ShortCV', 'CurrentEmployment', 'ModeofCommunication', 'PreviousExperience', 'DevelopmentAreas', 'OtherAreas', 'created_at', 'modified_at', 'last_login']
