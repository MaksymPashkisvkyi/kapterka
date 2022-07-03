from django.contrib import admin

from .models import Equipment, Contact, GroupAccounting, UserAccounting, RentedEquipment, GroupComposition, TypeOfHike


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_of_hike', 'unique', 'number', 'price_per_day',
                    'price', 'price_for_members', 'description')
    list_display_links = ('id', 'name')
    list_editable = ('unique',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_club_member', 'phone_number')


# TODO add equipment
@admin.register(GroupAccounting)
class GroupAccountingAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead_name', 'type_of_hike', 'responsible_person', 'group_composition',
                    'start_date', 'end_date', 'price', 'archived')


# TODO add equipment
@admin.register(UserAccounting)
class UserAccountingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'start_date', 'end_date', 'archived')


@admin.register(RentedEquipment)
class RentedEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipment', 'amount', 'type_of_accounting', 'user_accounting', 'group_accounting')


@admin.register(GroupComposition)
class GroupCompositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'realMembers', 'students', 'newOnes', 'others')


@admin.register(TypeOfHike)
class TypeOfHikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
