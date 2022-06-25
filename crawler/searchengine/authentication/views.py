from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_auth.models import TokenModel
from django.contrib.auth.models import User as djUser

from authentication import serializers, models


def login(user):
    user.last_login = timezone.now()
    user.save()
    token, created = TokenModel.objects.get_or_create(user=user)
    return token.key


class Login(APIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = serializers.Login

    def get_serializer(self):
        return serializers.Login()

    def post(self, request):
        serializer = serializers.Login(data=request.data)
        if serializer.is_valid():
            try:
                user = djUser.objects.get(
                    username=serializer.validated_data['username']
                )
                if user.profile.check_password(
                        serializer.validated_data['password']
                ):
                    user.profile.tmp_code_expire = timezone.now()
                    user.profile.save()
                    return Response(
                        {
                            'token': login(user)
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    raise djUser.DoesNotExist
            except djUser.DoesNotExist:
                return Response(
                    {
                        'message': 'username or password is invalid or OPT password expired'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(
            {
                'message': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginRequest(APIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = serializers.GetMobileSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        serializer = serializers.GetMobileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = djUser.objects.get(username=serializer.validated_data.get('username'))
            except djUser.DoesNotExist:
                user = serializer.save()
            finally:
                if user.profile.send_tmp_code():
                    return Response(
                        {
                            'message': 'Code sent'
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'message': 'Too many requests'
                        },
                        status=status.HTTP_429_TOO_MANY_REQUESTS
                    )
        return Response(
            {
                'message': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class Profile(APIView):

    def get(self, request):
        serializer = serializers.ProfileSerializer(request.user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = serializers.ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user.profile, serializer.validated_data)
            return Response(
                {'message': 'profile edited'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
