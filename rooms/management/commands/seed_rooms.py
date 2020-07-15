from django_seed import Seed
from django.core.management.base import BaseCommand
from rooms.models import Room, RoomType, Photo, Amenity, Facility, HouseRule
from users.models import User
import random
from django.contrib.admin.utils import flatten

class Command(BaseCommand):
    help = 'This command creates many users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default = 1, type=int, help='how many users do you want to create'
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        all_users = User.objects.all()
        room_types = RoomType.objects.all()
        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        rules = HouseRule.objects.all()
        seeder.add_entity(Room, number, {
            'name': lambda x: seeder.faker.address(),
            'host': lambda x: random.choice(all_users),
            'room_type': lambda x:random.choice(room_types),
            'price': lambda x:random.randint(100, 10000)//100 * 100,
            'beds':lambda x:random.randint(1, 5),
            'bedrooms':lambda x:random.randint(1, 5),
            'baths':lambda x:random.randint(1, 5),
            'guests':lambda x:random.randint(1, 10)
        })
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))
        for pk in created_clean:
            room = Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 17)):
                Photo.objects.create(
                    caption = seeder.faker.sentence(),
                    room=room,
                    file=f'rooms_photos/{random.randint(1,31)}.webp',
                )
            for a in amenities:
                idx = random.randint(0,15)
                if idx % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                idx = random.randint(0,15)
                if idx % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                idx = random.randint(0,15)
                if idx % 2 == 0:
                    room.house_rules.add(r)
        self.stdout.write(self.style.SUCCESS(f'{number} rooms are created!'))
