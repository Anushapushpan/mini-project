from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Appointment, Book_status, Category, Service, Time_slot


# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'status', 'date', 'time', 'created_at', 'updated_at')


class Time_slotAdmin(admin.ModelAdmin):
    list_display = ('slot', 'status')
    list_editable = ['status']


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Book_status)
admin.site.register(Time_slot, Time_slotAdmin)
admin.site.register(Category)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'created_at')


admin.site.register(Service, ServiceAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "time", "approved")
    list_filter = ("approved", "date")
    ordering = ("date", "time")
    search_fields = ("user_email", "user_name")
