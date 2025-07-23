from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()

class Question(models.Model):
    text = models.TextField()
    
    def __str__(self):
        return self.text[:50]


class Option(models.Model):
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    enneagram_type = models.PositiveSmallIntegerField()  # مثلاً 1 تا 9

    def __str__(self):
        return f"{self.text} → Type {self.enneagram_type}"

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    result_type = models.IntegerField()
    answers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class EnneagramType(models.Model):
    TYPE_CHOICES = [
        (1, 'تیپ ۱: کمال‌گرا'),
        (2, 'تیپ ۲: یاری‌رسان'),
        (3, 'تیپ ۳: موفقیت‌طلب'),
        (4, 'تیپ ۴: فردگرا'),
        (5, 'تیپ ۵: جستجوگر'),
        (6, 'تیپ ۶: وفادار'),
        (7, 'تیپ ۷: خوش‌گذران'),
        (8, 'تیپ ۸: چالش‌گر'),
        (9, 'تیپ ۹: صلح‌طلب'),
    ]
    
    type_number = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, unique=True)
    title = models.CharField(max_length=100)
    short_description = models.TextField(max_length=200)
    main_image = models.ImageField(upload_to='enneagram_types/')
    
    # بخش‌های اصلی محتوا
    overview = RichTextField(verbose_name='معرفی کلی')
    strengths = RichTextField(verbose_name='نقاط قوت')
    weaknesses = RichTextField(verbose_name='نقاط ضعف')
    growth_tips = RichTextField(verbose_name='راهکارهای رشد')
    relationships = RichTextField(verbose_name='روابط')
    career_paths = RichTextField(verbose_name='مسیر شغلی')
    
    # متا دیتا
    famous_examples = models.TextField(verbose_name='افراد مشهور')
    color_code = models.CharField(max_length=7, default='#FFD700', verbose_name='کد رنگ')
    
    class Meta:
        verbose_name = 'تیپ انیاگرام'
        verbose_name_plural = 'تیپ‌های انیاگرام'
    
    def __str__(self):
        return f"تیپ {self.type_number}: {self.title}"