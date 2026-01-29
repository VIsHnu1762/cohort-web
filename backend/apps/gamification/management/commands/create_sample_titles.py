"""
Management command to initialize sample titles for the gamification system
"""
from django.core.management.base import BaseCommand
from apps.gamification.models import Title


class Command(BaseCommand):
    help = 'Create sample titles for the gamification system'

    def handle(self, *args, **options):
        titles_data = [
            {
                'name': 'The Consistent',
                'description': 'Completed all episodes without breaking streak',
                'vault_credit_cost': 50,
                'icon': '🔥',
                'rarity': 'rare'
            },
            {
                'name': 'The Ascender',
                'description': 'Achieved Ascension Bonus in 3 consecutive seasons',
                'vault_credit_cost': 100,
                'icon': '📈',
                'rarity': 'epic'
            },
            {
                'name': 'The Finisher',
                'description': 'Completed first season with 100% episode completion',
                'vault_credit_cost': 30,
                'icon': '✅',
                'rarity': 'common'
            },
            {
                'name': 'The Quality Champion',
                'description': 'Achieved Season Score above 1400',
                'vault_credit_cost': 150,
                'icon': '👑',
                'rarity': 'legendary'
            },
            {
                'name': 'Code Warrior',
                'description': 'Maintained perfect LeetCode streak for entire season',
                'vault_credit_cost': 80,
                'icon': '⚔️',
                'rarity': 'epic'
            },
            {
                'name': 'Social Impact Hero',
                'description': 'Completed exceptional SRI activities',
                'vault_credit_cost': 60,
                'icon': '🤝',
                'rarity': 'rare'
            },
            {
                'name': 'Career Ready',
                'description': 'Completed all CFC tasks with high quality',
                'vault_credit_cost': 70,
                'icon': '💼',
                'rarity': 'rare'
            },
            {
                'name': 'Learning Machine',
                'description': 'Completed 3+ CLT certifications in one season',
                'vault_credit_cost': 50,
                'icon': '📚',
                'rarity': 'rare'
            },
            {
                'name': 'Season Champion',
                'description': 'Achieved Rank 1 in a season',
                'vault_credit_cost': 200,
                'icon': '🏆',
                'rarity': 'legendary'
            },
            {
                'name': 'Elite Runner',
                'description': 'Achieved Top 3 in a season',
                'vault_credit_cost': 120,
                'icon': '🥇',
                'rarity': 'epic'
            },
        ]
        
        created_count = 0
        for title_data in titles_data:
            title, created = Title.objects.get_or_create(
                name=title_data['name'],
                defaults=title_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created title: {title.name}'))
            else:
                self.stdout.write(f'Title already exists: {title.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal titles created: {created_count}'))
