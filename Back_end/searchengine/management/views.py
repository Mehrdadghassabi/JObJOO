from django.http import HttpResponse, Http404

from django.views import View
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from management import models, serializers


class Robots(View):

    def get(self, request):
        robot = models.Robots.objects.first()
        if robot:
            return HttpResponse(
                robot.text,
                content_type='text/plain'
            )
        raise Http404


class About(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(
            serializers.AboutUs(models.AboutUs.objects.last()).data,
            status=status.HTTP_200_OK
        )


class Contact(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.ContactUs(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Your message sent'
                }
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
