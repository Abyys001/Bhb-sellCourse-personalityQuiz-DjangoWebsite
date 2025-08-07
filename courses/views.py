from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
import requests
from .models import Course, UserCourse, PurchaseRequest, Lesson

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'title': _("دوره‌ها"),
        'course_list_message': _("دوره‌های موجود را مشاهده کنید."),
    })

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    has_access = False
    if request.user.is_authenticated:
        has_access = UserCourse.objects.filter(user=request.user, course=course).exists()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'has_access': has_access,
        'title': course.title,
        'detail_message': _("شما به این دوره دسترسی دارید.") if has_access else _("برای دسترسی به محتوای این دوره باید آن را خریداری کنید."),
    })

@login_required
def purchase_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # بررسی اینکه آیا کاربر قبلاً این دوره را خریده است
    if UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.info(request, _("شما قبلاً این دوره را خریداری کرده‌اید."))
        return redirect('course_detail', course_id=course.id)
    
    lang = request.GET.get('lang', 'fa')
    
    return render(request, 'courses/purchase_guide.html', {
        'course': course,
        'title': _("راهنمای خرید دوره"),
        'lang': lang,   
        'purchase_guide_message': _("برای خرید این دوره، لطفاً با ما در تلگرام یا اینستاگرام تماس بگیرید."),
    })

@require_POST
@login_required
def confirm_purchase(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    UserCourse.objects.get_or_create(user=request.user, course=course)
    messages.success(request, _("دوره با موفقیت خریداری شد."))
    return redirect('course_detail', course_id=course.id)

@require_POST
@login_required
def submit_purchase_request(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # بررسی اینکه آیا کاربر قبلاً این دوره را خریده است
    if UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.info(request, _("شما قبلاً این دوره را خریداری کرده‌اید."))
        return redirect('course_detail', course_id=course.id)
    
    contact_method = request.POST.get('contact_method')
    contact_info = request.POST.get('contact_info')
    message = request.POST.get('message', '')
    
    if not contact_method or not contact_info:
        messages.error(request, _("لطفاً روش تماس و اطلاعات تماس را وارد کنید."))
        return redirect('purchase_course', course_id=course.id)
    
    # ایجاد درخواست خرید
    PurchaseRequest.objects.create(
        user=request.user,
        course=course,
        contact_method=contact_method,
        contact_info=contact_info,
        message=message
    )
    
    messages.success(request, _("درخواست خرید شما با موفقیت ثبت شد. به زودی با شما تماس خواهیم گرفت."))
    return redirect('course_detail', course_id=course.id)

@login_required
def buy_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.user.is_authenticated:
        amount = int(course.price)
        description = _("خرید دوره %(title)s") % {'title': course.title}
        callback_url = f"https://bhbrand.net/course/{pk}/verify/"

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": amount * 10,
            "callback_url": callback_url,
            "description": description,
        }

        try:
            res = requests.post(settings.ZARINPAL_SANDBOX_URL, json=data, timeout=10)
            response_data = res.json()
        except requests.RequestException:
            return HttpResponse(_("خطا در اتصال به درگاه پرداخت."))

        if response_data.get('data', {}).get('code') == 100:
            authority = response_data['data']['authority']
            return redirect(f"https://www.zarinpal.com/pg/StartPay/{authority}")
        else:
            return HttpResponse(_("خطا در ارتباط با درگاه پرداخت."))
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
            messages.error(request, _("خطا در اتصال به درگاه پرداخت."))
            return render(request, 'courses/payment_status.html', {
                'success': False,
                'message': _("خطا در ارتباط با زرین‌پال."),
            })

        if result.get('data') and result['data'].get('code') == 100:
            UserCourse.objects.get_or_create(user=request.user, course=course)
            messages.success(request, _("پرداخت با موفقیت انجام شد و دسترسی به دوره برای شما فعال گردید."))
            return redirect('course_detail', course_id=course.id)
        else:
            error_msg = result.get('errors', {}).get('message', _('پرداخت توسط درگاه تایید نشد.'))
            messages.error(request, error_msg)
            return render(request, 'courses/payment_status.html', {
                'success': False,
                'message': error_msg,
            })

    else:
        messages.warning(request, _("پرداخت توسط کاربر لغو شد."))
        return render(request, 'courses/payment_status.html', {
            'success': False,
            'message': _("شما پرداخت را لغو کردید."),
        })

@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # بررسی دسترسی کاربر به دوره
    has_access = UserCourse.objects.filter(user=request.user, course=course).exists()
    
    if not has_access:
        messages.error(request, _("شما به این درس دسترسی ندارید. لطفاً ابتدا دوره را خریداری کنید."))
        return redirect('course_detail', course_id=course.id)
    
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'has_access': has_access,
        'title': f"{course.title} - {lesson.title}",
    })
