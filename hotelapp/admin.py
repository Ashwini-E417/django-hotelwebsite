from django.contrib import admin
from hotelapp.models import Rooms,Roombooking
# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display=['id','rname','Location','City','Price']
    list_filter=['Price','Location','City']

class BookingAdmin(admin.ModelAdmin):
    list_display=['rid','cname','mob','email','checkin','checkout','adults','child','status']
    list_filter=['rid','status','checkin','checkout']

admin.site.register(Rooms,RoomAdmin)
admin.site.register(Roombooking,BookingAdmin)