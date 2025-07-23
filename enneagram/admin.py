from django.contrib import admin
from .models import Question, Option, EnneagramType



class OptionInline(admin.TabularInline):
    model = Option
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

admin.site.register(Question, QuestionAdmin)


class EnneagramTypeAdmin(admin.ModelAdmin):
    list_display = ('type_number', 'title', 'short_description')
    search_fields = ('title', 'overview')
    list_filter = ('type_number',)

admin.site.register(EnneagramType, EnneagramTypeAdmin)
