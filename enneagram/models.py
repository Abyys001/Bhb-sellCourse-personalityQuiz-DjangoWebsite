from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

# مدل پایه برای سوالات
class BaseQuestion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

# مدل سوالات فارسی
class PersianQuestion(BaseQuestion):
    text = models.TextField(verbose_name="متن سوال فارسی")
    
    def __str__(self):
        return f"FA: {self.text[:50]}..."

# مدل سوالات انگلیسی
class EnglishQuestion(BaseQuestion):
    text = models.TextField(verbose_name="English Question Text")
    
    def __str__(self):
        return f"EN: {self.text[:50]}..."

class Option(models.Model):
    persian_question = models.ForeignKey(
        PersianQuestion, 
        on_delete=models.CASCADE, 
        related_name='options',
        null=True,
        blank=True
    )
    english_question = models.ForeignKey(
        EnglishQuestion, 
        on_delete=models.CASCADE, 
        related_name='options',
        null=True,
        blank=True
    )
    
    text = models.CharField(max_length=255, verbose_name="متن گزینه")
    enneagram_type = models.PositiveSmallIntegerField(verbose_name="تیپ انیاگرام")
    
    @property
    def question(self):
        return self.persian_question or self.english_question
    
    def __str__(self):
        return f"{self.text} → Type {self.enneagram_type}"

# مدل نتایج تست (بدون تغییر)
class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    result_type = models.IntegerField(verbose_name="تیپ نتیجه")
    answers = models.JSONField(verbose_name="پاسخ‌ها")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "نتیجه تست"
        verbose_name_plural = "نتایج تست"

# مدل تیپ‌های انیاگرام (بدون تغییر)
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
    
    type_number = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, unique=True, verbose_name="شماره تیپ")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    short_description = models.TextField(max_length=200, verbose_name="توضیح کوتاه")
    main_image = models.ImageField(upload_to='enneagram_types/', verbose_name="تصویر اصلی")
    
    overview = RichTextField(verbose_name='معرفی کلی')
    strengths = RichTextField(verbose_name='نقاط قوت')
    weaknesses = RichTextField(verbose_name='نقاط ضعف')
    growth_tips = RichTextField(verbose_name='راهکارهای رشد')
    relationships = RichTextField(verbose_name='روابط')
    career_paths = RichTextField(verbose_name='مسیر شغلی')
    
    famous_examples = models.TextField(verbose_name='افراد مشهور')
    color_code = models.CharField(max_length=7, default='#FFD700', verbose_name='کد رنگ')
    
    class Meta:
        verbose_name = 'تیپ انیاگرام'
        verbose_name_plural = 'تیپ‌های انیاگرام'
    
    def __str__(self):
        return f"تیپ {self.type_number}: {self.title}"