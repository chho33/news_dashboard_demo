import os
import csv
import numpy as np
import dateutil.parser

def clean_int(data):
    try:
        return int(float(data))
    except ValueError:
        return None

def clean_date(data):
    d = dateutil.parser.parser(data)    
    if isinstance(d.info,str):
        return d.info
    else: return None

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    import django
    django.setup()
    from text.models import Content 
    with open("test.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            created = Content.objects.get_or_create(
                url=row['url'],
                title=row['title'],
                content=row['content'],
                type=row['type'],
                source=row['source'],
                date=clean_date(row['date']),
                author=row['author'],
                discussion_count=clean_int(row['discussion_count']),
                share_count=clean_int(row['share_count']),
                comment_count=clean_int(row['comment_count']) ,
                like_count=clean_int(row['like_count']),
                dislike_count=clean_int(row['dislike_count']) ,
                )
