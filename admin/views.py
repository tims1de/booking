from sqladmin import ModelView

from bookings.models import Bookings
from hotels.models import Hotels
from hotels.rooms.models import Rooms
from users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password, Users.booking]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    form_excluded_columns = ('booking',)


class BookingsAdmin(ModelView, model=Bookings):
    column_list = '__all__'
    name = "Бронирование"
    name_plural = "Бронирования"
    icon = "fa-solid fa-book"
    form_excluded_columns = ('total_cost', 'total_days', )


class RoomsAdmin(ModelView, model=Rooms):
    column_list = '__all__'
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"
    form_excluded_columns = ('booking',)


class HotelsAdmin(ModelView, model=Hotels):
    column_list = '__all__'
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"
    form_excluded_columns = ('rooms',)
