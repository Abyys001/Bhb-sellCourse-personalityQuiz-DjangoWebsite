from django.db import models
from django.conf import settings

# Create your models here.
# dore/models.py

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='course_images/', null=True, blank=True, verbose_name="تصویر")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
        
    def lessons_with_description_count(self):
        return self.lessons.filter(description__isnull=False).count()


class UserCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="دوره")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ خرید")

    class Meta:
        verbose_name = "دوره خریداری‌شده"
        verbose_name_plural = "دوره‌های خریداری‌شده"
        ordering = ['-purchased_at']


from django.db import models

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, verbose_name="دوره")
    title = models.CharField(max_length=200, verbose_name="عنوان درس")
    description = models.TextField(blank=True, verbose_name="توضیحات درس")
    video_url = models.URLField(blank=True, verbose_name="لینک ویدیو (اختیاری)")
    video_file = models.FileField(upload_to='lesson_videos/', blank=True, null=True, verbose_name="فایل ویدیو")
    attachment = models.FileField(upload_to='lesson_attachments/', blank=True, null=True, verbose_name="فایل ضمیمه")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    
    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "درس‌ها"
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار بررسی'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
        ('completed', 'تکمیل شده'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="دوره")
    contact_method = models.CharField(max_length=20, choices=[
        ('telegram', 'تلگرام'),
        ('instagram', 'اینستاگرام'),
    ], verbose_name="روش تماس")
    contact_info = models.CharField(max_length=100, verbose_name="اطلاعات تماس")
    message = models.TextField(blank=True, verbose_name="پیام")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "درخواست خرید"
        verbose_name_plural = "درخواست‌های خرید"
        ordering = ['-created_at']
    
    def __str__(self):
        user = self.user
        # اگر username وجود داشت
        if hasattr(user, 'username') and user.username:
            user_display = user.username
        # اگر email وجود داشت
        elif hasattr(user, 'email') and user.email:
            user_display = user.email
        # اگر phone_number وجود داشت
        elif hasattr(user, 'phone_number') and user.phone_number:
            user_display = user.phone_number
        else:
            user_display = str(user.pk)
        return f"{user_display} - {self.course.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        from .models import UserCourse
        # بررسی تغییر وضعیت به approved
        is_new = self.pk is None
        old_status = None
        if not is_new:
            old = type(self).objects.get(pk=self.pk)
            old_status = old.status
        super().save(*args, **kwargs)
        if (is_new and self.status == 'approved') or (old_status != 'approved' and self.status == 'approved'):
            UserCourse.objects.get_or_create(user=self.user, course=self.course)