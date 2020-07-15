from django_seed import Seed
from django.core.management.base import BaseCommand
from reviews.models import Review
from users.models import User
from rooms.models import Room
import random

class Command(BaseCommand):
    help = 'This command creates many reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default = 1, type=int, help='how many users do you want to create'
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        user = User.objects.all()
        room = Room.objects.all()
        seeder.add_entity(Review, number, {
            'accuracy':lambda x: random.randint(0,5),
            'communication':lambda x: random.randint(0,5),
            'cleanliness':lambda x: random.randint(0,5),
            'location':lambda x: random.randint(0,5),
            'check_in':lambda x: random.randint(0,5),
            'value':lambda x: random.randint(0,5),
            'room':lambda x: random.choice(room),
            'user':lambda x: random.choice(user)
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{number} reviews are created!'))
