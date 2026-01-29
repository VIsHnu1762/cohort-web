import os
import django
import json
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.apps import apps

# Get all models except ContentType and Permission
all_objects = []
for model in apps.get_models():
    if model not in [ContentType, Permission]:
        all_objects.extend(model.objects.all())

# Serialize with natural keys
data = serializers.serialize('json', all_objects, use_natural_foreign_keys=True, use_natural_primary_keys=True)

# Write with UTF-8 encoding
with open('backup_data.json', 'w', encoding='utf-8') as f:
    f.write(data)

print(f'✅ Exported {len(all_objects)} objects to backup_data.json')
