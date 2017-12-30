# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from infra.serializers import UserSerializer, RegistrationSerializer
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@renderer_classes((JSONRenderer,))
# @permission_classes((IsAuthenticated, ))
@csrf_exempt
def user_view(request, pk=None, format=None):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user = None
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)

        user.delete()
        return Response({}, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'PUT':
        user = None
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = RegistrationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)