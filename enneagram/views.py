from django.shortcuts import render, redirect, get_object_or_404
from .models import EnneagramType

# Create your views here.
# enneagram/views.py
from django.shortcuts import render
from .models import Question
from collections import Counter
from accounts.models import UserProfile

def enneagram_test(request):
    questions = Question.objects.prefetch_related('options').all()
    return render(request, 'enneagram/test.html', {'questions': questions})

def submit_test(request):
    if request.method == "POST":
        type_counter = Counter()
        
        for key, value in request.POST.items():
            if key.startswith("question_"):
                type_counter[value] += 1

        most_common_type = type_counter.most_common(1)[0][0] if type_counter else None

        if request.user.is_authenticated:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            if most_common_type is not None:
                profile.enneagram_type = int(most_common_type)
                profile.save()
        
        if most_common_type:
            return redirect('type_detail', type_number=most_common_type)
    
    return render(request, "enneagram/test.html")



def type_detail(request, type_number):
    enneagram_type = get_object_or_404(EnneagramType, type_number=type_number)
    
    # پیشنهاد تیپ‌های مرتبط
    related_types = EnneagramType.objects.exclude(type_number=type_number).order_by('?')[:2]
    
    return render(request, 'enneagram/type_detail.html', {
        'type': enneagram_type,
        'related_types': related_types,
    })