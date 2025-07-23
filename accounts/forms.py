from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser


class RegisterForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100, required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'name']

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user




class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label="شماره تلفن",
        widget=forms.TextInput(attrs={
            'placeholder': '09123456789',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        password = cleaned_data.get('password')

        if phone_number and password:
            user = authenticate(
                phone_number=phone_number,
                password=password
            )
            if user is None:
                raise forms.ValidationError("شماره تلفن یا رمز عبور نامعتبر است")
            if not user.is_active:
                raise forms.ValidationError("این حساب کاربری غیرفعال شده است")
            cleaned_data['user'] = user
        return cleaned_data
