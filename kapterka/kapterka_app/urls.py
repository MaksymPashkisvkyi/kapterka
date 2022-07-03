from django.urls import path

from .views import CreateUser, AddEquipment, AddGroupAccounting, AddUserAccounting, HomePage

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("new_contact", CreateUser.as_view(), name="new_contact"),
    path("add_equipment", AddEquipment.as_view(), name="add_equipment"),
    path("group_accounting", AddGroupAccounting.as_view(), name="group_accounting"),
    path("user_accounting", AddUserAccounting.as_view(), name="user_accounting"),
]
