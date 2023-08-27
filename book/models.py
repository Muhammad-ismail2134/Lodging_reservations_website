import datetime
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models
from datetime import date
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    pass


class Offer(models.Model):
    a_title = models.CharField(max_length=100)
    a_content = models.CharField(max_length=200)
    a_img = models.ImageField(
        upload_to="book/media/photos", default="book/media/photos/appartment.jpg"
    )


class Name(models.Model):
    a_selfname = models.CharField(max_length=50)
    a_companyname = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.a_selfname} by {self.a_companyname}"


class Address(models.Model):
    a_address = models.CharField(max_length=200)
    a_zipcode = models.CharField(max_length=15, blank=True)
    a_city = models.CharField(max_length=100)
    a_country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.a_address} , {self.a_city},{self.a_country}"


class Facilities(models.Model):
    a_wifi = models.BooleanField(default=False)
    a_parking = models.BooleanField(default=False)
    a_family_rooms = models.BooleanField(default=False)
    a_room_service = models.BooleanField(default=False)
    a_fitness = models.BooleanField(default=False)
    a_bar = models.BooleanField(default=False)
    a_pool = models.BooleanField(default=False)


class AdvertCard(models.Model):
    a_category = models.CharField(max_length=10)
    a_name = models.ForeignKey(Name, on_delete=models.CASCADE, related_name="name")
    a_description = models.CharField(max_length=500)
    a_detail = models.CharField(max_length=1000, blank=True)
    a_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True, related_name="address"
    )
    a_img = models.ImageField(upload_to="book/media/photos")
    a_facilites = models.ForeignKey(
        Facilities,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="facilities",
    )
    a_price = models.FloatField(default=0)
    is_booked = models.BooleanField(default=False, null=True, blank=True)
    a_rating = models.FloatField(default=0, null=True)
    is_visited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.a_name} is {self.a_category} in {self.a_address.a_city}"


class RoomCategory(models.Model):
    a_category = models.CharField(
        max_length=10, blank=True, null=True, default="B Grade"
    )
    a_description = models.CharField(max_length=150, blank=True)
    a_price = models.FloatField(default=0)
    a_guests = models.SmallIntegerField(default=2, null=True)
    a_building = models.ForeignKey(
        AdvertCard, on_delete=models.CASCADE, related_name="building"
    )

    def __str__(self):
        return f"{self.a_category} rooms of {self.a_building}"


class Review(models.Model):
    a_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="commentUser",
    )
    a_message = models.CharField(max_length=100, default=0)
    a_rating = models.PositiveIntegerField(default=0, blank=True)
    a_building = models.ForeignKey(
        AdvertCard,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="advertCommentedOn",
    )
    a_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.a_author} review on {self.a_building.a_name.a_selfname} at {self.a_date.strftime('%d %b %Y %H:%H:%S')}"


class Suggestion(models.Model):
    a_message = models.CharField(max_length=200)
    a_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.a_message} on {self.a_date.strftime('%d %b %Y %H:%H:%S')}"


class Card(models.Model):
    a_holder_name = models.CharField(max_length=50)
    a_card_number = models.SmallIntegerField()
    a_expiry_date = models.DateField()
    a_cvc = models.SmallIntegerField()

    def __str__(self):
        return f"{self.a_holder_name} card"


class TableCategory(models.Model):
    a_category = models.CharField(
        max_length=10, blank=True, null=True, default="B Grade"
    )
    a_description = models.CharField(max_length=150, blank=True)
    a_table_for = models.SmallIntegerField(default=2, null=True)
    a_building = models.ForeignKey(
        AdvertCard, on_delete=models.CASCADE, related_name="Resturant"
    )

    def __str__(self):
        return f"{self.a_category} rooms of {self.a_building}"


class Booking(models.Model):
    a_booker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booker")
    a_booker_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="bokkerAddress"
    )
    a_guest = models.CharField(max_length=50, blank=True, null=True)
    a_request = models.CharField(max_length=300, blank=True, null=True)
    a_arrival = models.TimeField(blank=True, null=True)
    a_booker_phone_no = models.CharField(max_length=16, null=True)
    a_booker_card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name="bookerCard", null=True, blank=True
    )
    a_building = models.ForeignKey(
        AdvertCard, on_delete=models.CASCADE, related_name="place", null=True
    )
    a_payment = models.IntegerField(null=True, blank=True)
    a_time_date = models.DateTimeField(auto_now_add=True, null=True)
    a_booked_from = models.DateField(null=True, blank=True)
    a_booked_till = models.DateField(null=True, blank=True)
    a_finsished = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking made by {self.a_booker} on {self.a_time_date.strftime('%d %b %Y %H:%H:%S')}"


class Room(models.Model):
    a_roomNo = models.PositiveIntegerField(default=0)
    is_booked = models.BooleanField(default=False)
    a_booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, null=True, blank=True
    )
    a_booked_from = models.DateField(null=True)
    a_booked_till = models.DateField(null=True)
    a_category = models.ForeignKey(
        RoomCategory, on_delete=models.CASCADE, null=True, related_name="category"
    )

    def is_free(self):
        if self.a_booked_till is not None:
            if date.today() > self.a_booked_till:
                self.is_booked = False
                if self.a_booking is not None:
                    self.a_booking.a_finsished = True

    def __str__(self):
        return f"Room No.{self.a_roomNo} of {self.a_category.a_building.a_name}"


class Table(models.Model):
    a_tableNo = models.PositiveIntegerField(default=0, null=True)
    a_booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, null=True, related_name="booking"
    )
    is_booked = models.BooleanField(default=False, null=True)
    a_booked_from = models.DateTimeField(null=True)
    a_booked_till = models.DateTimeField(null=True)
    a_category = models.ForeignKey(
        TableCategory, on_delete=models.CASCADE, null=True, related_name="category"
    )

    def is_free(self):
        if self.a_booked_till is not None:
            current_datetime = timezone.now()
            current_datetime = current_datetime.replace(
                tzinfo=self.a_booked_till.tzinfo
            )

            if current_datetime > self.a_booked_till:
                self.is_booked = False
                if self.a_booking is not None:
                    self.a_booking.a_finsished = True
