from django.test import TestCase

# Create your tests here.
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KnowGoodsBack.settings.dev')
    import django
    django.setup()
    from applet.models import order,order_detail

