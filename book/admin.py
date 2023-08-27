from django.contrib import admin
from .models import (
    User,
    Offer,
    AdvertCard,
    Name,
    Room,
    Table,
    RoomCategory,
    TableCategory,
    Booking,
    Card,
    Review,
    Facilities,
)

# Register your models here.
admin.site.register(User),
admin.site.register(Offer),
admin.site.register(Name),
admin.site.register(Room),
admin.site.register(RoomCategory),
admin.site.register(TableCategory),
admin.site.register(Table),
admin.site.register(AdvertCard),
admin.site.register(Booking),
admin.site.register(Card),
admin.site.register(Review)
admin.site.register(Facilities)
