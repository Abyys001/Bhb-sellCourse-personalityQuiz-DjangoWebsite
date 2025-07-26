import os
import django
import json
from django.conf import settings

# تنظیم مسیر پروژه
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# تنظیم محیط Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bhbrand.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"  # برای حل مشکل async

# تنظیم مسیر فایل‌های settings
settings_file_path = os.path.join(BASE_DIR, 'Bhbrand', 'settings.py')
if os.path.exists(settings_file_path):
    settings.configure()
    
django.setup()

from django.contrib.contenttypes.models import ContentType
from enneagram.models import PersianQuestion, EnglishQuestion, Option

def import_english_questions():
    """وارد کردن سوالات انگلیسی"""
    with open('eg_questions.json', 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    en_content_type = ContentType.objects.get_for_model(EnglishQuestion)
    
    for question_data in questions_data:
        en_question = EnglishQuestion.objects.create(text=question_data['text'])
        
        for option_data in question_data['options']:
            Option.objects.create(
                content_type=en_content_type,
                object_id=en_question.id,
                text=option_data['text'],
                enneagram_type=option_data['enneagram_type']
            )
    
    print("✅ سوالات انگلیسی با موفقیت وارد شدند!")

def import_persian_questions():
    """وارد کردن سوالات فارسی"""
    with open('fa_questions.json', 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    fa_content_type = ContentType.objects.get_for_model(PersianQuestion)
    
    for question_data in questions_data:
        fa_question = PersianQuestion.objects.create(text=question_data['text'])
        
        for option_data in question_data['options']:
            Option.objects.create(
                content_type=fa_content_type,
                object_id=fa_question.id,
                text=option_data['text'],
                enneagram_type=option_data['enneagram_type']
            )
    
    print("✅ سوالات فارسی با موفقیت وارد شدند!")

if __name__ == '__main__':
    print("در حال وارد کردن سوالات...")
    try:
        import_english_questions()
        import_persian_questions()
        print("✅ عملیات با موفقیت به پایان رسید!")
    except Exception as e:
        print(f"❌ خطا در وارد کردن داده‌ها: {str(e)}")