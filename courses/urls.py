from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<int:course_id>/purchase/', views.purchase_course, name='purchase_course'),
    path('courses/<int:course_id>/confirm/', views.confirm_purchase, name='confirm_purchase'),
    path('courses/<int:course_id>/submit-request/', views.submit_purchase_request, name='submit_purchase_request'),
    path('course/<int:pk>/buy/', views.buy_course, name='buy_course'),
    path('course/<int:pk>/verify/', views.verify, name='verify'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



