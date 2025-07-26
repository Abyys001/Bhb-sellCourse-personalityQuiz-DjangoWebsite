from django.shortcuts import render, redirect, get_object_or_404
from .models import EnneagramType, PersianQuestion, EnglishQuestion, Option
from collections import Counter
from accounts.models import UserProfile
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType


def enneagram_test(request):
    lang = request.GET.get('lang', 'fa')
    if lang == 'en':
        questions = EnglishQuestion.objects.prefetch_related('options').all()
    else:
        questions = PersianQuestion.objects.prefetch_related('options').all()
    return render(request, 'enneagram/test.html', {
        'questions': questions,
        'lang': lang,
    })

def submit_test(request):
    lang = request.POST.get('lang', 'fa')
    if request.method == "POST":
        type_counter = Counter()
        
        if lang == 'en':
            questions = EnglishQuestion.objects.all()
        else:
            questions = PersianQuestion.objects.all()

        for q in questions:
            option_id = request.POST.get(f"question_{q.id}")
            if option_id:
                try:
                    option = Option.objects.get(id=option_id)
                    type_counter[str(option.enneagram_type)] += 1
                except Option.DoesNotExist:
                    continue

        most_common_type = type_counter.most_common(1)[0][0] if type_counter else None

        if request.user.is_authenticated:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            if most_common_type is not None:
                profile.enneagram_type = int(most_common_type)
                profile.save()
        
        if most_common_type:
            return redirect('type_detail', type_number=most_common_type)
    
    # اگر POST نبود یا نتیجه‌ای نبود، دوباره تست را با پیام نمایش بده
    if lang == 'en':
        questions = EnglishQuestion.objects.prefetch_related('options').all()
    else:
        questions = PersianQuestion.objects.prefetch_related('options').all()

    return render(request, "enneagram/test.html", {
        'questions': questions,
        'lang': lang,
        'title': _("تست اینیاگرام") if lang == 'fa' else _("Enneagram Test"),
        'test_message': _("لطفاً به سوالات زیر پاسخ دهید تا تیپ اینیاگرام خود را کشف کنید.") if lang == 'fa' else _("Please answer the following questions to discover your Enneagram type."),
        'error_message': _("لطفاً به همه سوالات پاسخ دهید.") if request.method == "POST" else "",
    })

def type_detail(request, type_number):
    enneagram_type = get_object_or_404(EnneagramType, type_number=type_number)
    
    # پیشنهاد تیپ‌های مرتبط
    related_types = EnneagramType.objects.exclude(type_number=type_number).order_by('?')[:2]
    
    return render(request, 'enneagram/type_detail.html', {
        'type': enneagram_type,
        'related_types': related_types,
        'title': _("تیپ اینیاگرام %(type_number)s") % {'type_number': enneagram_type.type_number},
        'related_types_message': _("ممکن است به این تیپ‌های مرتبط نیز علاقه‌مند باشید:"),
    })