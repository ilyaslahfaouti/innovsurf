from django.contrib import admin

from .models import CustomUser, Monitor, SurfClub, Surfer, EquipmentType, Equipment, SurfSpot, \
    LessonSchedule, SurfLesson, EquipmentSelection, Order, OrderItem, Forum, Message, Photo, Contact

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Monitor)
admin.site.register(SurfClub)
admin.site.register(Surfer)
admin.site.register(EquipmentType)
admin.site.register(Equipment)
admin.site.register(SurfSpot)
admin.site.register(LessonSchedule)
admin.site.register(SurfLesson)
admin.site.register(EquipmentSelection)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Forum)
admin.site.register(Message)
admin.site.register(Photo)
admin.site.register(Contact)

