from django.db import models
from core import models as core_models
from django_countries.fields import CountryField

# Create your models here.

class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class RoomType(AbstractItem):

    """ Room Type Model Definition """

    class Meta:
        verbose_name = 'Room Type'
        ordering = ['name']

class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = 'Amenities'

class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = 'Facilities'

class HouseRule(AbstractItem):

    """ House Rule Model Definition """

    class Meta:
        verbose_name = 'House Rule'

class Photo(core_models.TimeStampedModel):
    """ Photo model definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return self.caption

class Room(core_models.TimeStampedModel):

    """ Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    guests = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey('RoomType', on_delete=models.SET_NULL, null=True, related_name='rooms')
    amenities = models.ManyToManyField('Amenity', blank=True, related_name='rooms')
    facilities = models.ManyToManyField('Facility', blank=True, related_name='rooms')
    house_rules = models.ManyToManyField('HouseRule', blank=True, related_name='rooms')

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        print(all_reviews)
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
            if len(all_reviews) > 0:
                print(len(all_reviews))
                return all_ratings / len(all_reviews)
            else:
                return 0
