from django.contrib import admin
from .models import PersianQuestion, EnglishQuestion, Option, EnneagramType

# اگر از Inline استفاده می‌کنید، دو کلاس جداگانه برای سوالات فارسی و انگلیسی ایجاد کنید
class PersianOptionInline(admin.TabularInline):
    model = Option
    fk_name = 'persian_question'  # مشخص کردن فیلد ForeignKey
    extra = 1

class EnglishOptionInline(admin.TabularInline):
    model = Option
    fk_name = 'english_question'  # مشخص کردن فیلد ForeignKey
    extra = 1

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'enneagram_type', 'get_question')
    list_filter = ('enneagram_type',)
    search_fields = ('text',)
    
    def get_question(self, obj):
        return obj.persian_question or obj.english_question
    get_question.short_description = 'Question'

# ثبت مدل‌های سوال با Inline مربوطه
@admin.register(PersianQuestion)
class PersianQuestionAdmin(admin.ModelAdmin):
    inlines = [PersianOptionInline]
    list_display = ('id', 'text')

@admin.register(EnglishQuestion)
class EnglishQuestionAdmin(admin.ModelAdmin):
    inlines = [EnglishOptionInline]
    list_display = ('id', 'text')

@admin.register(EnneagramType)
class EnneagramTypeAdmin(admin.ModelAdmin):
    list_display = ('type_number', 'title', 'short_description')