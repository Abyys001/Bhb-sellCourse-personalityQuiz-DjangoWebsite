from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Lesson, UserCourse

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('order', 'title', 'video_url', 'video_file', 'description')
    ordering = ('order',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('title', 'price', 'created_at', 'lessons_count')
    search_fields = ('title', 'description')
    # prepopulated_fields = {'slug': ('title',)}  # اگر slug field دارید
    
    def lessons_count(self, obj):
        return obj.lessons.count()
    lessons_count.short_description = "تعداد درس‌ها"

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_link', 'video_link')
    list_filter = ('course',)
    search_fields = ('title', 'description')
    
    def course_link(self, obj):
        return format_html('<a href="/admin/courses/course/{}/change/">{}</a>',
                          obj.course.id,
                          obj.course.title)
    course_link.short_description = "دوره"
    
    def video_link(self, obj):
        if obj.video_url:
            return format_html('<a href="{}" target="_blank">تماشا</a>', obj.video_url)
        elif obj.video_file:
            return format_html('<a href="{}" target="_blank">دانلود</a>', obj.video_file.url)
        return "-"
    video_link.short_description = "لینک ویدیو"

admin.site.register(UserCourse)