from django.core.cache import cache
from django.core.management.base import BaseCommand

from app import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        best_tags = models.Tag.objects.get_top()
        cache.set('best_tags', best_tags, 20)
        best_members = models.Profile.objects.get_top()
        cache.set('best_members', best_members, 20)