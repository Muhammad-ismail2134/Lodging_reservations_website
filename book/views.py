from math import floor
from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import date
from django.urls import reverse
from .models import (
    User,
    Offer,
    AdvertCard,
    Name,
    Address,
    Room,
    RoomCategory,
    TableCategory,
    Table,
    Booking,
    Card,
    Review,
    Facilities,
)

# Create your views here.


def index(request):
    offers = Offer.objects.all().order_by().reverse()
    user = request.user
    # Checking Whether the rooms booking is expired or not
    rooms = Room.objects.all()
    tables = Table.objects.all()
    bookings = Booking.objects.all()
    categories = AdvertCard.objects.values_list("a_category", flat=True).distinct()
    cities = AdvertCard.objects.values_list("a_address__a_city", flat=True).distinct()
    countries = AdvertCard.objects.values_list(
        "a_address__a_country", flat=True
    ).distinct()
    visited_cards = AdvertCard.objects.filter(is_visited=True).order_by("id").reverse()
    for room in rooms:
        room.is_free()
        room.save()
    for table in tables:
        table.is_free()
        table.save()
    for booking in bookings:
        current_date = date.today()
        if booking.a_booked_till is not None:
            if current_date > booking.a_booked_till:
                booking.a_building.is_booked = False
                booking.a_building.save()
                booking.a_finsished = True
                booking.save()

    finished_booking = []
    for booking in bookings:
        if booking.a_finsished == True:
            finished_booking.append(booking)

    return render(
        request,
        "book/index.html",
        {
            "offers": offers,
            "bookings": finished_booking,
            "visited_cards": visited_cards,
            "categories": categories,
            "cities": cities,
            "countries": countries,
            "user": user,
        },
    )


def search(request):
    if request.method == "GET":
        city = request.GET.get("search_city")
        persons = request.GET.get("person")
        advertList = []
        addresses = []
        AllCards = AdvertCard.objects.all()
        for card in AllCards:
            addresses.append(card.a_address)
        buildings = AdvertCard.objects.filter(
            a_address__a_city__contains=city, is_booked=False
        )
        for building in buildings:
            advertList.append(building)

        # For hotels
        try:
            hotel_rooms_unbooked = Room.objects.filter(
                a_category__a_building__a_address__a_city=city, is_booked=False
            )
            hotelList = []
            for room in hotel_rooms_unbooked:
                hotels = AdvertCard.objects.filter(
                    a_name__a_selfname=room.a_category.a_building
                ).distinct()
                hotelList.append(hotels)

            for hotel in hotelList:
                rooms = Room.objects.filter(a_category__a_building=hotel)
                no_of_guests = 0
                for room in rooms:
                    no_of_guests += room.a_guest
                if no_of_guests >= persons:
                    advertList.append(hotel)
        except:
            pass
        rating_list = []
        for card in advertList:
            customer_reviews = Review.objects.filter(a_building=card)
            rating_sum = 0
            for review in customer_reviews:
                rating_sum += review.a_rating
            if customer_reviews.count() > 0:
                rating_avg = rating_sum / customer_reviews.count()
                card.a_rating = floor(rating_avg)
            else:
                card.a_rating = 0
            rating_list.append(range(card.a_rating))

        return render(
            request,
            "book/book.html",
            {
                "AllCards": advertList,
                "rating_list": rating_list,
                "addresses": addresses,
            },
        )
    return render(request, "book/index.html")


def advert(request, id):
    card = AdvertCard.objects.get(pk=id)
    card_image = card.a_img
    card.is_visited = True
    card.save()
    customer_reviews = Review.objects.filter(a_building=card)
    rating_list = []
    for review in customer_reviews:
        rating_list.append(range(review.a_rating))
    try:
        room_categorys = RoomCategory.objects.filter(a_building=card)
        rooms_list = []
        rooms_count_list = []

        for category in room_categorys:
            rooms = Room.objects.filter(a_category=category, is_booked=False)
            room_count = Room.objects.filter(
                a_category=category, is_booked=False
            ).count()
            rooms_list.append(rooms)
            rooms_count_list.append(room_count)
    except RoomCategory.DoesNotExist:
        room_categorys = None
    try:
        table_categorys = TableCategory.objects.filter(a_building=card)
        table_count_list = []
        tables_list = []
        for category in table_categorys:
            tables = Table.objects.filter(a_category=category, is_booked=False)
            tables_count = Table.objects.filter(
                a_category=category, is_booked=False
            ).count()
            tables_list.append(tables)
            table_count_list.append(tables_count)
    except TableCategory.DoesNotExist:
        table_categorys = None

    if room_categorys:
        guest = 2
        A_grade, B_grade, C_grade = rooms_count_list
        return render(
            request,
            "book/advert.html",
            {
                "card": card,
                "card_image": card_image,
                "room_categorys": room_categorys,
                "rooms": rooms_list,
                "rooms_count": rooms_count_list,
                "guest": guest,
                "reviews": customer_reviews,
                "A_grade": range(A_grade),
                "B_grade": range(B_grade),
                "C_grade": range(C_grade),
                "rating_list": rating_list,
            },
        )
    elif table_categorys:
        guest = 3
        vip, gold, common = table_count_list
        return render(
            request,
            "book/advert.html",
            {
                "card": card,
                "guest": guest,
                "card_image": card_image,
                "table_categorys": table_categorys,
                "tables": tables_list,
                "tables_count": table_count_list,
                "VIP": range(vip),
                "Gold": range(gold),
                "Common": range(common),
                "reviews": customer_reviews,
                "rating_list": rating_list,
            },
        )
    else:
        return render(
            request,
            "book/advert.html",
            {
                "card": card,
                "card_image": card_image,
                "reviews": customer_reviews,
                "rating_list": rating_list,
            },
        )


def book(request):
    Allcards = AdvertCard.objects.filter(is_booked=False)
    rating_list = []
    addresses = []

    for card in Allcards:
        customer_reviews = Review.objects.filter(a_building=card)
        address = card.a_address
        addresses.append(address)
        rating_sum = 0
        for review in customer_reviews:
            rating_sum += review.a_rating
        if customer_reviews.count() > 0:
            rating_avg = rating_sum / customer_reviews.count()
            card.a_rating = floor(rating_avg)
        else:
            card.a_rating = 0
        rating_list.append(range(card.a_rating))
    addresses = list(set(addresses))

    return render(
        request,
        "book/book.html",
        {"AllCards": Allcards, "rating_list": rating_list, "addresses": addresses},
    )


def detail(request, id):
    card = AdvertCard.objects.get(pk=id)
    return render(request, "book/detail.html", {"card": card})


def userBooking(request, id):
    user = User.objects.get(pk=id)
    bookings = Booking.objects.filter(a_booker=user).order_by("id").reverse()
    rooms_list = []
    tables_list = []
    for book in bookings:
        tables = Table.objects.filter(a_booking=book)
        rooms = Room.objects.filter(a_booking=book)
        rooms_list.append(rooms)
        tables_list.append(tables)

    return render(
        request,
        "book/userBooking.html",
        {
            "user": user,
            "bookings": bookings,
            "rooms_list": rooms_list,
            "tables_list": tables_list,
        },
    )


def admin(request):
    bookings = Booking.objects.all().order_by("id").reverse()
    reviews = Review.objects.all().order_by("id").reverse()
    offers = Offer.objects.all()
    rooms_list = []
    tables_list = []
    rating_list = []

    for book in bookings:
        tables = Table.objects.filter(a_booking=book)
        rooms = Room.objects.filter(a_booking=book)
        rooms_list.append(rooms)
        tables_list.append(tables)
    for review in reviews:
        rating_list.append(range(review.a_rating))
    return render(
        request,
        "book/admin.html",
        {
            "bookings": bookings,
            "rooms_list": rooms_list,
            "tables_list": tables_list,
            "reviews": reviews,
            "rating_list": rating_list,
            "offers": offers,
        },
    )


def makeOffer(request):
    if request.method == "POST":
        title = request.POST["offer-title"]
        content = request.POST["offer-detail"]
        img = request.FILES["offer-img"]
        offer = Offer(a_title=title, a_content=content, a_img=img)
        offer.save()
        return HttpResponseRedirect(reverse("index"))


def deleteOffer(request):
    if request.method == "GET":
        title = request.GET.get("offer-title")
        try:
            offer = Offer.objects.get(a_title=title)
            offer.delete()
        except:
            pass
        return HttpResponseRedirect(reverse("index"))


def addAdvertCard(request):
    if request.method == "POST":
        # Get data
        self_name = request.POST["selfName"]
        company = request.POST["company"]
        address = request.POST["address"]
        category = request.POST.get("category")
        description = request.POST["description"]
        detail = request.POST["detail"]
        city = request.POST["city"]
        country = request.POST["country"]
        img = request.FILES["image-upload"]

        # Facilites
        wifi = request.POST.get("wifi")
        parking = request.POST.get("parking")
        service = request.POST.get("service")
        pool = request.POST.get("pool")
        fitness = request.POST.get("fitness")
        bar = request.POST.get("bar")
        family = request.POST.get("family")

        facilities = Facilities(
            a_wifi=wifi,
            a_parking=parking,
            a_family_rooms=family,
            a_room_service=service,
            a_bar=bar,
            a_pool=pool,
        )
        facilities.save()

        name = Name(a_selfname=self_name, a_companyname=company)
        name.save()
        address = Address(a_address=address, a_city=city, a_country=country)
        address.save()
        Advert = AdvertCard(
            a_category=category,
            a_name=name,
            a_description=description,
            a_detail=detail,
            a_address=address,
            a_img=img,
            a_facilities=facilities,
        )
        Advert.save()
        room_list = []
        if category == "Hotel":
            # Creating categories
            a_descrip = request.POST["aGradeDescription"]
            a_price = request.POST["aGradePricePerRoom"]
            a_number = request.POST["aGradeNoOfRooms"]
            a_room_for = request.POST["A_room_for"]
            aRoomCategory = RoomCategory(
                a_category="A Grade",
                a_description=a_descrip,
                a_price=a_price,
                a_building=Advert,
                a_guest=a_room_for,
            )
            aRoomCategory.save()
            b_descrip = request.POST["bGradeDescription"]
            b_price = request.POST["bGradePricePerRoom"]
            b_number = request.POST["bGradeNoOfRooms"]
            b_room_for = request.POST["B_room_for"]
            bRoomCategory = RoomCategory(
                a_category="B Grade",
                a_description=b_descrip,
                a_price=b_price,
                a_building=Advert,
                a_guest=b_room_for,
            )
            bRoomCategory.save()
            c_descrip = request.POST["cGradeDescription"]
            c_price = request.POST["cGradePricePerRoom"]
            c_number = request.POST["cGradeNoOfRooms"]
            c_room_for = request.POST["C_room_for"]
            cRoomCategory = RoomCategory(
                a_category="C Grade",
                a_description=c_descrip,
                a_price=c_price,
                a_building=Advert,
                a_guest=c_room_for,
            )
            cRoomCategory.save()

            # Creating instances of room
            roomNo = 1
            for i in range(int(a_number)):
                room_list.append(Room(a_roomNo=roomNo, a_category=aRoomCategory))
                roomNo = roomNo + 1

            for i in range(int(b_number)):
                room_list.append(Room(a_roomNo=roomNo, a_category=bRoomCategory))
                roomNo = roomNo + 1

            for i in range(int(c_number)):
                room_list.append(Room(a_roomNo=roomNo, a_category=cRoomCategory))
                roomNo = roomNo + 1
            Room.objects.bulk_create(room_list)

        # For Resturants Table
        # VIp

        elif category == "Resturant":
            vip_descrip = request.POST["VIPdescription"]
            gold_descrip = request.POST["Golddescription"]
            common_descrip = request.POST["commonDescription"]
            vip_number = request.POST["VIPNoOfRooms"]
            gold_number = request.POST["GoldNoOfRooms"]
            common_number = request.POST["commonNoOfRooms"]
            vip_table_for = request.POST["vip_table_for"]
            gold_table_for = request.POST["gold_table_for"]
            common_table_for = request.POST["common_table_for"]

            vipTableCategory = TableCategory(
                a_category="VIP",
                a_description=vip_descrip,
                a_building=Advert,
                a_table_for=vip_table_for,
            )
            vipTableCategory.save()

            goldTableCategory = TableCategory(
                a_category="Gold",
                a_description=gold_descrip,
                a_building=Advert,
                a_table_for=gold_table_for,
            )
            goldTableCategory.save()

            commonTableCategory = TableCategory(
                a_category="Common",
                a_description=common_descrip,
                a_building=Advert,
                a_table_for=common_table_for,
            )
            commonTableCategory.save()
            table_no = 0
            table_list = []
            for i in range(int(vip_number)):
                table_list.append(
                    Table(a_tableNo=table_no, a_category=vipTableCategory)
                )
                table_no += 1

            for i in range(int(gold_number)):
                table_list.append(
                    Table(a_tableNo=table_no, a_category=goldTableCategory)
                )
                table_no += 1
            for i in range(int(common_number)):
                table_list.append(
                    Table(a_tableNo=table_no, a_category=commonTableCategory)
                )
                table_no += 1
            Table.objects.bulk_create(table_list)
        else:
            price = request.POST["wholePrice"]
            Advert.a_price = price
            Advert.save()

        return HttpResponseRedirect(reverse("book"))


def removeAdvertCard(request):
    if request.method == "POST":
        # Get data
        self_name = request.POST["selfName"]
        company = request.POST["company"]
        address = request.POST["address"]
        try:
            card = AdvertCard.objects.get(a_address__a_address=address)
            card.delete()
        except AdvertCard.DoesNotExist:
            return render(
                request, "book/book.html", {"message": "Such object does not exists"}
            )
        return render(
            request, "book/book.html", {"message": "Object deleted successfully"}
        )


# Making a booking
def makeBooking(request, id):
    if request.method == "POST":
        building = AdvertCard.objects.get(pk=id)
        if building.a_category == "Hotel":
            aGrade = request.POST["A_grade_rooms"]
            bGrade = request.POST["B_grade_rooms"]
            cGrade = request.POST["C_grade_rooms"]
            A_category = RoomCategory.objects.get(
                a_category="A Grade", a_building=building
            )
            B_category = RoomCategory.objects.get(
                a_category="B Grade", a_building=building
            )
            C_category = RoomCategory.objects.get(
                a_category="C Grade", a_building=building
            )
            all_aGrade_rooms = Room.objects.filter(
                a_category=A_category, is_booked=False
            )
            all_bGrade_rooms = Room.objects.filter(
                a_category=B_category, is_booked=False
            )
            all_cGrade_rooms = Room.objects.filter(
                a_category=C_category, is_booked=False
            )
            user = request.user
            guest_name = request.POST["guest_name"]
            user_request = request.POST["customer_request"]
            arrival_time = request.POST["arrival_time"]
            address = request.POST["customer_address"]
            city = request.POST["customer_address_city"]
            country = request.POST["customer_address_country"]
            zipcode = request.POST["customer_address_zipcode"]
            phone = request.POST["customer_phone"]
            payment = request.POST["total-payment"]
            booked_from = request.POST["booked_from"]
            booked_till = request.POST["booked_till"]
            # making Booking address object
            booker_address = Address(
                a_address=address, a_city=city, a_country=country, a_zipcode=zipcode
            )
            booker_address.save()
            try:
                card_holder_name = request.POST["card_holder_name"]
                card_number = request.POST["card_number"]
                card_expiry_date = request.POST["card_expiry_date"]
                card_cvc = request.POST["card_cvc"]

                customer_card = Card(
                    a_holder_name=card_holder_name,
                    a_card_number=card_number,
                    a_expiry_date=card_expiry_date,
                    a_cvc=card_cvc,
                )
                customer_card.save()
                booking = Booking(
                    a_booker=user,
                    a_booker_address=booker_address,
                    a_guest=guest_name,
                    a_request=user_request,
                    a_arrival=arrival_time,
                    a_booker_phone_no=phone,
                    a_booker_card=customer_card,
                    a_building=building,
                    a_payment=payment,
                    a_booked_from=booked_from,
                    a_booked_till=booked_till,
                )
                booking.save()
            except:
                booking = Booking(
                    a_booker=user,
                    a_booker_address=booker_address,
                    a_guest=guest_name,
                    a_request=user_request,
                    a_arrival=arrival_time,
                    a_booker_phone_no=phone,
                    a_building=building,
                )
                booking.save()
            #
            # updating Rooms objects
            counter = 0
            for room in all_aGrade_rooms:
                if counter > int(aGrade):
                    break
                else:
                    room.a_booking = booking
                    room.is_booked = True
                    room.a_booked_from = booked_from
                    room.a_booked_till = booked_till
                    room.save()
                counter += 1
            counter = 0
            for room in all_bGrade_rooms:
                if counter > int(bGrade):
                    break
                else:
                    room.a_booking = booking
                    room.is_booked = True
                    room.a_booked_from = booked_from
                    room.a_booked_till = booked_till
                    room.save()
                counter += 1
            for room in all_cGrade_rooms:
                if counter > int(cGrade):
                    break
                else:
                    room.a_booking = booking
                    room.is_booked = True
                    room.a_booked_from = booked_from
                    room.a_booked_till = booked_till
                    room.save()
                counter += 1
        ## For Resturants
        elif building.a_category == "Resturant":
            vip = request.POST["VIP"]
            gold = request.POST["Gold"]
            common = request.POST["Common"]
            vip_category = TableCategory.objects.get(
                a_category="VIP", a_building=building
            )
            gold_category = TableCategory.objects.get(
                a_category="Gold", a_building=building
            )
            Common_category = TableCategory.objects.get(
                a_category="Common", a_building=building
            )
            all_vip_tables = Table.objects.filter(
                a_category=vip_category, is_booked=False
            )
            all_gold_tables = Table.objects.filter(
                a_category=gold_category, is_booked=False
            )
            all_common_tables = Table.objects.filter(
                a_category=Common_category, is_booked=False
            )
            user = request.user
            guest_name = request.POST["guest_name"]
            user_request = request.POST["customer_request"]
            address = request.POST["customer_address"]
            city = request.POST["customer_address_city"]
            country = request.POST["customer_address_country"]
            zipcode = request.POST["customer_address_zipcode"]
            phone = request.POST["customer_phone"]
            booked_from = request.POST["booked_from"]
            booked_till = request.POST["booked_till"]
            # making Booking address object
            booker_address = Address(
                a_address=address, a_city=city, a_country=country, a_zipcode=zipcode
            )
            booker_address.save()

            booking = Booking(
                a_booker=user,
                a_booker_address=booker_address,
                a_guest=guest_name,
                a_request=user_request,
                a_booker_phone_no=phone,
                a_building=building,
            )
            booking.save()
            #
            # updating Rooms objects
            counter = 0
            for table in all_vip_tables:
                if counter > int(vip):
                    break
                else:
                    table.a_booking = booking
                    table.is_booked = True
                    table.a_booked_from = booked_from
                    table.a_booked_till = booked_till
                    table.save()
                counter += 1
            counter = 0
            for table in all_gold_tables:
                if counter > int(gold):
                    break
                else:
                    table.a_booking = booking
                    table.is_booked = True
                    table.a_booked_from = booked_from
                    table.a_booked_till = booked_till
                    table.save()
                counter += 1
            for table in all_common_tables:
                if counter > int(common):
                    break
                else:
                    table.a_booking = booking
                    table.is_booked = True
                    table.a_booked_from = booked_from
                    table.a_booked_till = booked_till
                    table.save()
                counter += 1
        else:
            user = request.user
            guest_name = request.POST["guest_name"]
            user_request = request.POST["customer_request"]
            arrival_time = request.POST["arrival_time"]
            address = request.POST["customer_address"]
            city = request.POST["customer_address_city"]
            country = request.POST["customer_address_country"]
            zipcode = request.POST["customer_address_zipcode"]
            phone = request.POST["customer_phone"]
            payment = request.POST["total-payment"]
            booked_from = request.POST["booked_from"]
            booked_till = request.POST["booked_till"]
            # making Booking address object
            booker_address = Address(
                a_address=address, a_city=city, a_country=country, a_zipcode=zipcode
            )
            booker_address.save()
            try:
                card_holder_name = request.POST["card_holder_name"]
                card_number = request.POST["card_number"]
                card_expiry_date = request.POST["card_expiry_date"]
                card_cvc = request.POST["card_cvc"]

                customer_card = Card(
                    a_holder_name=card_holder_name,
                    a_card_number=card_number,
                    a_expiry_date=card_expiry_date,
                    a_cvc=card_cvc,
                )
                customer_card.save()
                booking = Booking(
                    a_booker=user,
                    a_booker_address=booker_address,
                    a_guest=guest_name,
                    a_request=user_request,
                    a_arrival=arrival_time,
                    a_booker_phone_no=phone,
                    a_booker_card=customer_card,
                    a_building=building,
                    a_payment=payment,
                )
                booking.save()
            except:
                booking = Booking(
                    a_booker=user,
                    a_booker_address=booker_address,
                    a_guest=guest_name,
                    a_request=user_request,
                    a_arrival=arrival_time,
                    a_booker_phone_no=phone,
                    a_building=building,
                )
                booking.save()

        return HttpResponseRedirect(reverse(userBooking, kwargs={"id": user.id}))


def review(request, id):
    if request.method == "POST":
        author = request.user
        message = request.POST["message"]
        rating = request.POST["rating"]
        booking = Booking.objects.get(pk=id)
        building = booking.a_building
        customer_review = Review(
            a_author=author,
            a_message=message,
            a_rating=rating,
            a_building=building,
        )
        customer_review.save()
        booking.delete()
    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "book/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "book/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "book/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        auth_login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "book/register.html")
