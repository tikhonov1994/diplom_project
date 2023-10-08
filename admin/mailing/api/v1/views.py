from rest_framework.views import APIView
from uuid import UUID
from rest_framework.exceptions import ParseError
from mailing.models import Template
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from mailing.serializers import TemplateSerializer


class TemplateDataView(APIView):

    def get(self, request, q: str):
        try:
            query = {'id': UUID(q)}
        except ValueError:
            query = {'name': q}
        try:
            template = Template.objects.get(**query)
        except Template.DoesNotExist:
            return HttpResponse('', status=status.HTTP_404_NOT_FOUND)
        serializer = TemplateSerializer(template)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)