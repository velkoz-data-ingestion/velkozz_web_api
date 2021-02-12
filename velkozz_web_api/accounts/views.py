# Importing Django Packages:
from django.shortcuts import render
from rest_framework import viewsets
from django.db import models

from rest_framework.permissions import IsAuthenticated
from .permissions import HasAPIAccess

class AbstractModelViewSet(viewsets.ModelViewSet):
    """A ModelViewSet object that serves as an abstract
    ModelViewSet for all ViewSets used in the REST APIs in
    the project.

    This object is not intended to serve as an actual initalized
    ModelViewSet, just as a parent for other methods.
    """
    # Adding Custom Permissions for the ModelViewSet:
    permission_classes = [IsAuthenticated, HasAPIAccess]


def site_main_index(request):
    context = {}
    return render(request, "accounts/site_index.html", context)


def account_index(request):
    context = {}

    # Populating the Context:
    context["user"] = request.user

    return render(request, "accounts/account_index.html", context)