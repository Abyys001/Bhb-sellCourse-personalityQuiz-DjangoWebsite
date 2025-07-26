from django.db import models

# Create your models here.

class SampleModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام نمونه")

    class Meta:
        verbose_name = "مدل نمونه"
        verbose_name_plural = "مدل‌های نمونه"

    def __str__(self):
        return self.name
