# import os, sys
# import django

# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(project_root)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mppp.settings')
# django.setup()


# from scraper.models import Category, Tender

# uts = Tender.objects.filter(category__label=None)
# i = 0
# n = len(uts)
# print(f"Found items: {n:05}\n")

# deleted_count, _ = uts.delete()
# print(f"Deleted {deleted_count} objects")
