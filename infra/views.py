# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from infra.models import BarberUser
from infra.serializers import BarberUserSerializer

# Create your views here.
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated, ))
@csrf_exempt
def users_list(request):
    if request.method == 'GET':
        users = BarberUser.objects.all()
        serializer = BarberUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
