from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("book", views.book, name="book"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("adminM", views.admin, name="adminM"),
    path("addAdvertCard", views.addAdvertCard, name="addAdvertCard"),
    path("removeAdvertCard", views.removeAdvertCard, name="removeAdvertCard"),
    path("<int:id>", views.advert, name="advert"),
    path("review/<int:id>", views.review, name="review"),
    path("makeOffer", views.makeOffer, name="makeOffer"),
    path("search", views.search, name="search"),
    path("userBooking/<int:id>", views.userBooking, name="userBooking"),
    path("makeBooking/<int:id>", views.makeBooking, name="makeBooking"),
]
