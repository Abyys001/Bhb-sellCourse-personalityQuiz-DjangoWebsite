from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Lesson, UserCourse, PurchaseRequest

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

@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'purchased_at')
    list_filter = ('course', 'purchased_at')
    search_fields = ('user__phone_number', 'user__name', 'course__title')
    readonly_fields = ('purchased_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'course')

@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'contact_method', 'status', 'created_at', 'has_access')
    list_filter = ('status', 'contact_method', 'created_at')
    search_fields = ('user__username', 'user__email', 'course__title')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'course')
    
    def has_access(self, obj):
        """نمایش وضعیت دسترسی کاربر به دوره"""
        has_access = UserCourse.objects.filter(user=obj.user, course=obj.course).exists()
        if has_access:
            return format_html('<span style="color: green;">✓ دسترسی فعال</span>')
        else:
            return format_html('<span style="color: red;">✗ بدون دسترسی</span>')
    has_access.short_description = "وضعیت دسترسی"
    
    def approve_request(self, request, queryset):
        """تایید درخواست و فعال‌سازی دسترسی به دوره"""
        approved_count = 0
        for purchase_request in queryset:
            if purchase_request.status != 'approved':
                purchase_request.status = 'approved'
                purchase_request.save()
                # ایجاد دسترسی کاربر به دوره
                UserCourse.objects.get_or_create(user=purchase_request.user, course=purchase_request.course)
                approved_count += 1
        if approved_count > 0:
            self.message_user(request, f"{approved_count} درخواست تایید و دسترسی به دوره فعال شد.")
        else:
            self.message_user(request, "هیچ درخواست جدیدی تایید نشد.")
    approve_request.short_description = "تایید درخواست و فعال‌سازی دسترسی"
    
    def activate_course_access(self, request, queryset):
        """فعال‌سازی دسترسی به دوره برای درخواست‌های انتخاب شده"""
        activated_count = 0
        for purchase_request in queryset:
            # ایجاد دسترسی کاربر به دوره (صرف نظر از وضعیت درخواست)
            user_course, created = UserCourse.objects.get_or_create(
                user=purchase_request.user, 
                course=purchase_request.course
            )
            if created:
                activated_count += 1
        if activated_count > 0:
            self.message_user(request, f"دسترسی به دوره برای {activated_count} کاربر فعال شد.")
        else:
            self.message_user(request, "همه کاربران قبلاً دسترسی داشتند.")
    activate_course_access.short_description = "فعال‌سازی دسترسی به دوره"
    
    def complete_request(self, request, queryset):
        """تکمیل درخواست‌های انتخاب شده"""
        queryset.update(status='completed')
        self.message_user(request, f"{queryset.count()} درخواست تکمیل شد.")
    complete_request.short_description = "تکمیل درخواست‌های انتخاب شده"
    
    def reject_request(self, request, queryset):
        """رد درخواست‌های انتخاب شده"""
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} درخواست رد شد.")
    reject_request.short_description = "رد درخواست‌های انتخاب شده"
    
    def add_user_to_purchased_courses(self, request, queryset):
        """افزودن کاربر به لیست دوره‌های خریداری‌شده (بدون تغییر وضعیت درخواست)"""
        added_count = 0
        for purchase_request in queryset:
            user_course, created = UserCourse.objects.get_or_create(
                user=purchase_request.user,
                course=purchase_request.course
            )
            if created:
                added_count += 1
        if added_count > 0:
            self.message_user(request, f"{added_count} کاربر به لیست دوره‌های خریداری‌شده اضافه شد.")
        else:
            self.message_user(request, "همه کاربران قبلاً در لیست دوره‌های خریداری‌شده بودند.")
    add_user_to_purchased_courses.short_description = "افزودن کاربر به لیست دوره‌های خریداری‌شده"
    
    actions = ['approve_request', 'activate_course_access', 'complete_request', 'reject_request', 'add_user_to_purchased_courses']