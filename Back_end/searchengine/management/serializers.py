from rest_framework import serializers
from drf_recaptcha.fields import ReCaptchaV3Field

from management import models


class AboutUs(serializers.ModelSerializer):
    class Meta:
        model = models.AboutUs
        fields = '__all__'


class ContactUs(serializers.ModelSerializer):
    recaptcha = ReCaptchaV3Field(
        'contact'
    )

    class Meta:
        model = models.ContactUs
        fields = '__all__'

    def validate(self, attrs):
        print(11111)
        attrs.pop("recaptcha")
        return super(ContactUs, self).validate(attrs)
