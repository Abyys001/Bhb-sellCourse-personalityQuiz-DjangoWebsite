"""
URL configuration for Bhbrand project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # فعال‌سازی تغییر زبان
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += i18n_patterns(
    path('', include('pages.urls')),
    path('', include('enneagram.urls')),
    path('', include('courses.urls')),
)