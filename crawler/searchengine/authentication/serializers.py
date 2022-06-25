from django.contrib.auth.models import User as djUser
from django.utils import timezone

from authentication.exceptions import InvalidCode, PasswordNotMatch
from authentication.models import ProfileModel

from rest_framework import serializers


class Login(serializers.Serializer):
    username = serializers.RegexField(
        r'(09)[0-9]{9}',
        required=True
    )
    password = serializers.CharField(required=True)


class GetMobileSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r'(09)[0-9]{9}',
    )

    class Meta:
        model = djUser

        fields = (
            'username',
        )


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    credit = serializers.ReadOnlyField()

    class Meta:
        model = ProfileModel
        fields = (
            'first_name',
            'last_name',
            'email',
            'address',
            'province',
            'city',
            'avatar',
            'credit'
        )

    def update(self, instance, validated_data):
        if validated_data.get('user', None):
            for (key, value) in validated_data.pop('user').items():
                setattr(instance.user, key, value)
            instance.user.save()
        super(ProfileSerializer, self).update(instance, validated_data)


# class Register(serializers.Serializer):
#     username = serializers.RegexField(
#         r'(09)[0-9]{9}',
#         required=True
#     )
#     password1 = serializers.CharField(required=True)
#     password2 = serializers.CharField(required=True)
#     tmp_code = serializers.CharField(required=True)
#
#     def validate(self, args):
#         try:
#             user = djUser.objects.get(username=args['username'])
#             if user.profile.tmp_code != args['tmp_code'] or \
#                     user.profile.tmp_code_expire < timezone.now():
#                 raise InvalidCode
#             if args['password1'] != args['password2']:
#                 raise PasswordNotMatch
#             return args
#         except djUser.DoesNotExist:
#             raise serializers.ValidationError(
#                 {'username': 'Does not exist'}
#             )
#         except InvalidCode:
#             raise serializers.ValidationError(
#                 {'tmp_code': 'Invalid or expired'}
#             )
#         except PasswordNotMatch:
#             raise serializers.ValidationError(
#                 {'password': 'Passwords not match'}
#             )
#
#     def save(self, **kwargs):
#         try:
#             user = djUser.objects.get(
#                 username=self.validated_data['username']
#             )
#             user.set_password(self.validated_data['password1'])
#             user.profile.tmp_code_expire = timezone.now()
#             user.save()
#             user.profile.save()
#             return user
#         except djUser.DoesNotExist:
#             raise serializers.ValidationError(
#                 {'username': 'Does not exist'}
#             )
