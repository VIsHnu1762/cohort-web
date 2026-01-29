"""
Management command to sync LeetCode streaks for all students
Run daily via cron: python manage.py sync_leetcode_streaks
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.gamification.models import Season
from apps.gamification.services import LeetCodeSyncService


class Command(BaseCommand):
    help = 'Sync LeetCode streaks for all students in current season'

    def add_arguments(self, parser):
        parser.add_argument(
            '--season-id',
            type=int,
            help='Specific season ID to sync (defaults to current active season)',
        )

    def handle(self, *args, **options):
        season_id = options.get('season_id')
        
        if season_id:
            try:
                season = Season.objects.get(id=season_id)
            except Season.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Season {season_id} not found'))
                return
        else:
            season = Season.objects.filter(
                is_active=True,
                start_date__lte=timezone.now().date(),
                end_date__gte=timezone.now().date()
            ).first()
        
        if not season:
            self.stdout.write(self.style.ERROR('No active season found'))
            return
        
        self.stdout.write(f'Starting LeetCode sync for {season.name}...')
        
        results = LeetCodeSyncService.sync_all_students(season)
        
        self.stdout.write(self.style.SUCCESS(
            f'Sync completed!\n'
            f'Success: {results["success"]}\n'
            f'Failed: {results["failed"]}'
        ))
        
        if results['errors']:
            self.stdout.write(self.style.WARNING('Errors:'))
            for error in results['errors'][:10]:  # Show first 10 errors
                self.stdout.write(f'  - {error}')
