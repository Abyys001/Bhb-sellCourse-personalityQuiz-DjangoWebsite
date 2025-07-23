from django.db import models
from django.conf import settings

# Create your models here.
# dore/models.py

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        
    def lessons_with_description_count(self):
        return self.lessons.filter(description__isnull=False).count()


class UserCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)


from django.db import models

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, verbose_name="لینک ویدیو (اختیاری)")
    video_file = models.FileField(upload_to='lesson_videos/', blank=True, null=True, verbose_name="فایل ویدیو")
    attachment = models.FileField(upload_to='lesson_attachments/', blank=True, null=True, verbose_name="فایل ضمیمه")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"