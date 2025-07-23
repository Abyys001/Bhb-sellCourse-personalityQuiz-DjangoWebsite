from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests
from .models import Course, UserCourse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Course, UserCourse
import requests

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})



from .models import UserCourse

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    has_access = False
    if request.user.is_authenticated:
        has_access = UserCourse.objects.filter(user=request.user, course=course).exists()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'has_access': has_access,
    })

    

@require_POST
def purchase_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    UserCourse.objects.get_or_create(user=request.user, course=course)
    return redirect('course_detail', course_id=course.id)



def buy_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.user.is_authenticated:
        amount = int(course.price)
        description = f"خرید دوره {course.title}"
        callback_url = f"https://bhbrand.net/course/{pk}/verify/"

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": amount * 10,
            "callback_url": callback_url,
            "description": description,
        }

        res = requests.post(settings.ZARINPAL_SANDBOX_URL, json=data)
        response_data = res.json()

        if response_data['data']['code'] == 100:
            authority = response_data['data']['authority']
            return redirect(f"https://www.zarinpal.com/pg/StartPay/{authority}")
        else:
            return HttpResponse("خطا در ارتباط با درگاه")
    else:
        return redirect('login')




@login_required
def verify(request, pk):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    course = get_object_or_404(Course, pk=pk)

    if status == 'OK':
        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": int(course.price) * 10,
            "authority": authority,
        }

        try:
            res = requests.post(settings.ZARINPAL_VERIFY_URL, json=data, timeout=10)
            result = res.json()
        except requests.RequestException:
            messages.error(request, "خطا در اتصال به درگاه پرداخت.")
            return render(request, 'courses/payment_status.html', {'success': False, 'message': "خطا در ارتباط با زرین‌پال."})

        if result.get('data') and result['data'].get('code') == 100:
            UserCourse.objects.get_or_create(user=request.user, course=course)
            messages.success(request, "پرداخت با موفقیت انجام شد. دسترسی به دوره فعال شد.")
            return redirect('course_detail', course_id=course.id)
        else:
            error_msg = result.get('errors', {}).get('message', 'پرداخت تایید نشد توسط درگاه.')
            messages.error(request, error_msg)
            return render(request, 'courses/payment_status.html', {'success': False, 'message': error_msg})

    else:
        messages.warning(request, "پرداخت توسط کاربر لغو شد.")
        return render(request, 'courses/payment_status.html', {'success': False, 'message': "شما پرداخت را لغو کردید."})


@login_required
def purchase_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if not UserCourse.objects.filter(user=request.user, course=course).exists():
        UserCourse.objects.create(user=request.user, course=course)

    return redirect('course_detail', course_id=course.id)
