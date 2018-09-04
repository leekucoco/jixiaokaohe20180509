# -*- coding: utf-8 -*-
__author__ = 'bobby'
from rest_framework import permissions
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user



class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsPerformanceAdminUser(permissions.BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        burusergroup = Group.objects.get(name="基层绩效考核员")
        users = User.objects.filter(groups=burusergroup)
        if request.user in users or request.user.is_superuser:
            return True
        else:
            return False