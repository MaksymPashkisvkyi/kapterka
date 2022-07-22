from datetime import datetime
from json import loads

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from .models import Contact
from .models import Equipment
from .models import GroupAccounting
from .models import GroupComposition
from .models import RentedEquipment
from .models import UserAccounting


def base_context(request, **args):
    context = {'title': 'none', 'header': 'none', 'error': 0}

    if args is not None:
        for arg in args:
            context[arg] = args[arg]
    return context


def get_all_contacts():
    contacts = []
    for contact in Contact.objects.all():
        contacts.append((contact.id, contact.name, contact.phone_number))
    return contacts


def beauty_date_interval(date1: datetime, date2: datetime, show_year=False, show_if_this_year=False):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    result = ''
    result += str(date1.day) + ' '

    if (date1.day, date1.month, date1.year) == (date2.day, date2.month, date2.year):
        result += months[date1.month - 1]
    else:
        if date1.month == date2.month:
            result += '- ' + str(date2.day) + ' ' + months[date1.month - 1]
        else:
            result += months[date1.month - 1] + ' - ' + \
                      str(date2.day) + ' ' + months[date2.month - 1]

    if show_year:
        if show_if_this_year:
            result += ', ' + str(date1.year)
        else:
            if date1.year != datetime.now().year:
                result += ', ' + str(date1.year)

    return result


def get_all_free_equipment():
    eq_list = []
    for equipment in Equipment.objects.all():
        eq_list.append((equipment.id,
                        equipment.name,
                        equipment.type_of_hike,
                        equipment.description,
                        equipment.price_per_day,
                        equipment.price_for_members,
                        equipment.number))
        # TODO Append filters to filter only free equipment
    return eq_list


class HomePage(View):

    @staticmethod
    def get(request):
        context = base_context(request, title='Home')
        group_accounting_list = list(
            GroupAccounting.objects.order_by("-id")[:30])
        group_accounting = list(map(lambda acc: (acc, beauty_date_interval(
            acc.start_date, acc.end_date), RentedEquipment.objects.filter(group_accounting=acc)),
                                    group_accounting_list))
        user_accounting_list = list(
            UserAccounting.objects.order_by("-id")[:30])
        user_accounting = list(map(lambda acc: (acc, beauty_date_interval(
            acc.start_date, acc.end_date), RentedEquipment.objects.filter(group_accounting=acc)), user_accounting_list))
        context["accountings"] = user_accounting + group_accounting
        return render(request, "home.html", context)


class CreateUser(View):

    @staticmethod
    def get(request):
        context = base_context(
            request, title='Новый контакт', header='Добавить нового пользователя')
        return render(request, "add_contact.html", context)

    @staticmethod
    def post(request):
        form = request.POST

        name_input = form['name_input']
        number_input = form['number_input']
        in_club_input = form['in_club_input'] == "on"

        contact = Contact(
            name=name_input,
            phone_number=number_input,
            is_club_member=in_club_input,
        )

        contact.save()

        return HttpResponseRedirect("/new_contact")


class AddEquipment(View):
    def get(self, request):
        context = base_context(
            request, title='Записать снар на группу', header='Запись снаряжения на группу')
        return render(request, "add_equipment.html", context)

    def post(self, request):
        return HttpResponseRedirect("/")


class AddGroupAccounting(View):
    def get(self, request):
        context = base_context(
            request, title='Запись снаряжения на группу', header='Запись снаряжения на группу')
        contacts_list = get_all_contacts()
        eq_list = get_all_free_equipment()
        context['eq_list'] = eq_list
        context['contacts_list'] = contacts_list
        return render(request, "new_group_accounting.html", context)

    def post(self, request):
        form = request.POST

        group_composition = GroupComposition(
            realMembers=form['realMembers'],
            students=form['students'],
            newOnes=form['newOnes'],
            others=form['others']
        )
        group_composition.save()

        group_accounting = GroupAccounting(
            lead_name=form['leadName'],
            type_of_hike=form['typeOfHike'],
            responsible_person=Contact.objects.get(),
            group_composition=group_composition,
            start_date=form['startDate'],
            end_date=form['endDate'],
            price=form['price'],
            archived=False
        )
        group_accounting.save()

        equipment_json = loads(form['equipmentJSON'])

        for eqId in equipment_json:
            rentedEq = RentedEquipment(
                equipment=Equipment.objects.get(),
                amount=equipment_json[eqId],
                type_of_accounting="GroupAccounting",
                group_accounting=group_accounting
            )
            rentedEq.save()

        group_accounting.save()
        return HttpResponseRedirect("/")


class AddUserAccounting(View):
    def get(self, request):
        context = base_context(
            request, title='Записать снар на человека', header='Запись снаряжения на человека')
        contacts_list = get_all_contacts()
        eq_list = get_all_free_equipment()
        context['eq_list'] = eq_list
        context['contacts_list'] = contacts_list
        return render(request, "new_user_accounting.html", context)

    def post(self, request):
        form = request.POST
        user_accounting = UserAccounting(
            user=Contact.objects.get(),
            start_date=form['startDate'],
            end_date=form['endDate'],
            archived=False
        )
        user_accounting.save()
        equipment_json = loads(form['equipmentJSON'])

        for eqId in equipment_json:
            rentedEq = RentedEquipment(
                equipment=Equipment.objects.get(),
                amount=equipment_json[eqId],
                type_of_accounting="GroupAccounting",
                group_accounting=user_accounting
            )
            rentedEq.save()

        user_accounting.save()
        return HttpResponseRedirect("/")
