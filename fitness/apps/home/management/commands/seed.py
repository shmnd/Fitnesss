from django.core.management.base import BaseCommand
from apps.home.models import FitnessClass
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Seed data"

    def handle(self, *args, **kwargs):
        FitnessClass.objects.all().delete()
        now = timezone.now()
        classes = [
            {'fitness_name': 'Yoga', 'instructor': 'Alice', 'datetime': now + timedelta(days=1), 'total_slots': 10},
            {'fitness_name': 'Zumba', 'instructor': 'Bob', 'datetime': now + timedelta(days=2), 'total_slots': 8},
            {'fitness_name': 'HIIT', 'instructor': 'Carol', 'datetime': now + timedelta(days=3), 'total_slots': 12},
        ]
        for c in classes:
            FitnessClass.objects.create(**c, available_slots=c['total_slots'])
        self.stdout.write("Seeded fitness classes.")
