import os, sys, django
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mppp.settings')
django.setup()

from scraper.models import Agrement, Qualif

print("ssssssssssssssssssssssssssssssssss")
ags = Qualif.objects.all()
print(f"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa: { ags.count() }")

for ag in ags:
    print("============= ag.name ==============")
    # ag.save()
print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")