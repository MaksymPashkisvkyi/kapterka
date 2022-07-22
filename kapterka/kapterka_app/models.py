from django.db import models

TYPE_OF_HIKE = [
    ("ПВД", "noncategoried"),
    ("Лыжный", "лыжный"),
    ("Горный", "горный"),
    ("Водный", "водный"),
    ("Пеший", "пеший"),
    ("Спелео", "спелео"),
    ("Вело", "вело"),
]

TYPE_OF_ACCOUNTING = [
    ("UserAccounting", "GroupAccounting"),
    ("GroupAccounting", "GroupAccounting")
]


class TypeOfHike(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Вид туризма')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид туризма'
        verbose_name_plural = 'Виды туризма'
        ordering = ['id']


class Equipment(models.Model):
    name = models.CharField(max_length=250, default='карабин', verbose_name='Название снаряжения')
    type_of_hike = models.ForeignKey('TypeOfHike', on_delete=models.PROTECT, verbose_name='Вид туризма')
    unique = models.BooleanField(default=True, verbose_name='Уникальность')
    number = models.IntegerField(default=1, blank=True, verbose_name='Количество')
    price = models.IntegerField(default=0, blank=True, verbose_name='Стоимость')
    price_per_day = models.IntegerField(default=0, blank=True, verbose_name='Стоимость посуточная')
    price_for_members = models.IntegerField(default=0, blank=True,
                                            verbose_name='Стоимость посуточная для участников клуба')
    description = models.CharField(max_length=1000, default='', null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Снаряжение'
        verbose_name_plural = 'Снаряжение'
        ordering = ['id']


class Contact(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    is_club_member = models.BooleanField(default=False, verbose_name='Член клуба')
    phone_number = models.CharField(max_length=30, blank=True, verbose_name='Номер телефона')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['id']


class GroupComposition(models.Model):
    realMembers = models.IntegerField(default=0, verbose_name='Действительные члены')
    students = models.IntegerField(default=0, verbose_name='Студенты')
    newOnes = models.IntegerField(default=0, verbose_name='Новички')
    others = models.IntegerField(default=0, verbose_name='Остальные')

    class Meta:
        verbose_name = 'Члены клуба'
        verbose_name_plural = 'Члены клуба'
        ordering = ['id']


class GroupAccounting(models.Model):
    lead_name = models.CharField(max_length=250, default='Смерека', verbose_name='Руководитель группы')
    type_of_hike = models.CharField(max_length=15, choices=TYPE_OF_HIKE, default="ПВД", verbose_name='Вид похода')
    responsible_person = models.ForeignKey(Contact, null=True, default=None,
                                           related_name="responsible_person", on_delete=models.CASCADE,
                                           verbose_name='Ответственный человек')
    group_composition = models.ForeignKey(GroupComposition, null=True, default=None, related_name="group",
                                          on_delete=models.CASCADE, verbose_name='Group composition (изменить)')
    start_date = models.DateField(default="2021-01-02", verbose_name='Дата выдачи снаряжения')
    end_date = models.DateField(default="2021-01-02", verbose_name='Дата возврата снаряжения')
    equipment = models.ManyToManyField(Equipment, verbose_name='Снаряжение')
    price = models.IntegerField(default=0, null=False, verbose_name='Стоимость аренды')
    archived = models.BooleanField(default=False, verbose_name='Archived (изменить)')

    class Meta:
        verbose_name = 'Учёт снаряжения на группы'
        verbose_name_plural = 'Учёт снаряжения на группы'
        ordering = ['-end_date']


class UserAccounting(models.Model):
    user = models.ForeignKey(
        Contact, null=True, default=None, related_name="user", on_delete=models.CASCADE, verbose_name='Имя')
    start_date = models.DateField(default="2021-01-02", verbose_name='Дата выдачи снаряжения')
    end_date = models.DateField(default="2021-01-02", verbose_name='Дата возврата снаряжения')
    equipment = models.ManyToManyField(Equipment, verbose_name='Снаряжение')
    archived = models.BooleanField(default=False, verbose_name='Archived (изменить)')

    class Meta:
        verbose_name = 'Учёт снаряжения на человека'
        verbose_name_plural = 'Учёт снаряжения на человека'
        ordering = ['-end_date']


class RentedEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, null=True, default=None, related_name="equipment",
                                  on_delete=models.CASCADE, verbose_name='Снаряжение')
    amount = models.IntegerField(default=1, blank=True, verbose_name='Количество')
    type_of_accounting = models.CharField(max_length=15, choices=TYPE_OF_ACCOUNTING, default="GroupAccounting",
                                          verbose_name='Групповое или индивидуальное')
    user_accounting = models.ForeignKey(
        UserAccounting, null=True, default=None, on_delete=models.CASCADE, verbose_name='Запись на человека')
    group_accounting = models.ForeignKey(
        GroupAccounting, null=True, default=None, on_delete=models.CASCADE, verbose_name='Запись на группу')

    class Meta:
        verbose_name = 'Арендуемое снаряжение'
        verbose_name_plural = 'Арендуемое снаряжение'
        ordering = ['id']
