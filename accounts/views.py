from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from .forms import RegisterForm, LoginForm
from .models import UserProfile

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {
        "form": form,
        "title": _("ثبت نام"),
        "register_message": _("لطفاً فرم زیر را برای ثبت نام تکمیل کنید."),
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {
        'form': form,
        "title": _("ورود"),
        "login_message": _("لطفاً اطلاعات کاربری خود را وارد کنید."),
    })

def account_view(request):
    return render(request, "accounts/account.html", {
        "title": _("حساب کاربری"),
        "account_message": _("به صفحه حساب کاربری خود خوش آمدید."),
    }) 

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def user_dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    return render(request, "accounts/dashboard.html", {
        "user": request.user,
        "profile": profile,
        "title": _("داشبورد"),
        "dashboard_message": _("به داشبورد خود خوش آمدید."),
    })
