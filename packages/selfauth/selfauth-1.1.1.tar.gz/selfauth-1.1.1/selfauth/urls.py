""" URL definitions for the application. Used for testing purposes only. """

from django.conf import settings
from django.urls import include, path

from . import views

urlpatterns = [path("auth/", include("mozilla_django_oidc.urls"))]

# Adds test view if settings enables it.
if getattr(settings, "AUTH_TEST", False):
    url_path = getattr(settings, "AUTH_TEST_PATH", "")
    urlpatterns.append(path(url_path, views.TestView.as_view(), name="selfauth-test"))
