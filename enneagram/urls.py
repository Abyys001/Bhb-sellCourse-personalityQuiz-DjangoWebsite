from django.urls import path 
from . import views

urlpatterns = [
    path("enneagram_test/", views.enneagram_test, name="enneagram_test"),
    path("submit_test/", views.submit_test, name="submit_test"),
    path("type/<int:type_number>/", views.type_detail, name="type_detail"),
]   