import os
import django
from django.conf import settings

# تنظیم محیط Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bhbrand.settings')
django.setup()

from enneagram.models import Question, Option
import json

def import_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    for question_data in questions_data:
        question = Question.objects.create(text=question_data['text'])
        
        for option_data in question_data['options']:
            Option.objects.create(
                question=question,
                text=option_data['text'],
                enneagram_type=option_data['enneagram_type']
            )
    
    print("✅ سوالات و گزینه‌ها با موفقیت وارد شدند!")

if __name__ == '__main__':
    import_questions()