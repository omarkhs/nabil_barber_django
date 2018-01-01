# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from infra.serializers import UserSerializer
from infra.permissions import IsUserOwner
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (UserPermissions,)

    def get_permissions(self):
        permission_classes = []
        if self.action in ['update','partial_update']:
            permission_classes.append(IsUserOwner)

        return [permission() for permission in permission_classes]

    def login(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({'auth':'Authenticaion failed'}, status=status.HTTP_400_BAD_REQUEST)

    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

