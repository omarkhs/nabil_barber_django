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
from infra.serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login

@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@csrf_exempt
def login_view(request):
    username = request.POST.get('username', None);
    password = request.POST.get('password', None);
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({}, status=status.HTTP_200_OK)
    else:
        return Response({'auth':'Authenticaion failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PUT'])
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated, ))
@csrf_exempt
def user_view(request, pk=None, format=None):
    if request.method == 'GET':
        if request.user.is_authenticated():
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return Response({'auth':'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)

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

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


