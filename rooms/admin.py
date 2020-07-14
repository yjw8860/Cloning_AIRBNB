from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition"""

    list_display = (
        'name',
        'used_by'
    )

    def used_by(self, obj):
        return obj.rooms.count()

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition"""

    fieldsets = (
        (
            'Spaces',
            {'fields': ('guests', 'bedrooms', 'beds', 'baths')}
        ),
        (
            'Basic Info',
            {'fields':('name', 'description', 'country', 'address', 'price')}
        ),
        (
            'Times',
            {'fields':('check_in', 'check_out', 'instant_book')}
        ),
        (
            'More About the Space',
            {'fields':('amenities','facilities','house_rules',)}
        ),
        (
            'Last Details',
            {'fields':('host',)}
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        'count_photos',
        'total_rating'
    )

    list_filter = ('instant_book','host__superhost', "room_type", "amenities", "facilities", "house_rules", 'country', 'city')

    #https://docs.djangoproject.com/en/2.2/ref/contrib/admin/ 참고
    search_fields = ['=city', '^host__username']

    filter_horizontal = ('amenities','facilities','house_rules',)

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition"""

    list_display = (
        '__str__',
        'get_thumbnail'
    )

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width=50px height=50px src={obj.file.url} />')

    get_thumbnail.short_description = 'Thumbnail'