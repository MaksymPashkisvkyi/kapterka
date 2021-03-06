# Generated by Django 4.0.5 on 2022-06-17 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Имя')),
                ('is_club_member', models.BooleanField(default=False, verbose_name='Член клуба')),
                ('phone_number', models.CharField(blank=True, max_length=30, verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Контакт',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='карабин', max_length=250, verbose_name='Название снаряжения')),
                ('unique', models.BooleanField(default=True, verbose_name='Уникальность')),
                ('number', models.IntegerField(blank=True, default=1, verbose_name='Количество')),
                ('price', models.IntegerField(blank=True, default=0, verbose_name='Стоимость')),
                ('price_per_day', models.IntegerField(blank=True, default=0, verbose_name='Стоимость посуточная')),
                ('price_for_members', models.IntegerField(blank=True, default=0, verbose_name='Стоимость посуточная для участников клуба')),
                ('description', models.CharField(default='', max_length=1000, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Снаряжение',
                'verbose_name_plural': 'Снаряжение',
            },
        ),
        migrations.CreateModel(
            name='GroupAccounting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lead_name', models.CharField(default='Смерека', max_length=250, verbose_name='Руководитель группы')),
                ('type_of_hike', models.CharField(choices=[('ПВД', 'noncategoried'), ('Лыжный', 'лыжный'), ('Горный', 'горный'), ('Водный', 'водный'), ('Пеший', 'пеший'), ('Спелео', 'спелео'), ('Вело', 'вело')], default='ПВД', max_length=15, verbose_name='Вид похода')),
                ('start_date', models.DateField(default='2021-01-02', verbose_name='Дата выдачи снаряжения')),
                ('end_date', models.DateField(default='2021-01-02', verbose_name='Дата возврата снаряжения')),
                ('price', models.IntegerField(default=0, verbose_name='Стоимость аренды')),
                ('archived', models.BooleanField(default=False, verbose_name='Archived (изменить)')),
                ('equipment', models.ManyToManyField(to='kapterka_app.equipment', verbose_name='Снаряжение')),
            ],
            options={
                'verbose_name': 'Учёт снаряжения на группы',
                'verbose_name_plural': 'Учёт снаряжения на группы',
            },
        ),
        migrations.CreateModel(
            name='GroupComposition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realMembers', models.IntegerField(default=0, verbose_name='Действительные члены')),
                ('students', models.IntegerField(default=0, verbose_name='Студенты')),
                ('newOnes', models.IntegerField(default=0, verbose_name='Новички')),
                ('others', models.IntegerField(default=0, verbose_name='Остальные')),
            ],
            options={
                'verbose_name': 'Члены клуба',
                'verbose_name_plural': 'Члены клуба',
            },
        ),
        migrations.CreateModel(
            name='TypeOfHike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Вид туризма')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccounting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default='2021-01-02', verbose_name='Дата выдачи снаряжения')),
                ('end_date', models.DateField(default='2021-01-02', verbose_name='Дата возврата снаряжения')),
                ('archived', models.BooleanField(default=False, verbose_name='Archived (изменить)')),
                ('equipment', models.ManyToManyField(to='kapterka_app.equipment', verbose_name='Снаряжение')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='kapterka_app.contact', verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Учёт снаряжения на человека',
                'verbose_name_plural': 'Учёт снаряжения на человека',
            },
        ),
        migrations.CreateModel(
            name='RentedEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=1, verbose_name='Количество')),
                ('type_of_accounting', models.CharField(choices=[('UserAccounting', 'GroupAccounting'), ('GroupAccounting', 'GroupAccounting')], default='GroupAccounting', max_length=15, verbose_name='Групповое или индивидуальное')),
                ('equipment', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipment', to='kapterka_app.equipment', verbose_name='Снаряжение')),
                ('group_accounting', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='kapterka_app.groupaccounting', verbose_name='Запись на группу')),
                ('user_accounting', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='kapterka_app.useraccounting', verbose_name='Запись на человека')),
            ],
            options={
                'verbose_name': 'Арендуемое снаряжение',
                'verbose_name_plural': 'Арендуемое снаряжение',
            },
        ),
        migrations.AddField(
            model_name='groupaccounting',
            name='group_composition',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='kapterka_app.groupcomposition', verbose_name='Group composition (изменить)'),
        ),
        migrations.AddField(
            model_name='groupaccounting',
            name='responsible_person',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsible_person', to='kapterka_app.contact', verbose_name='Ответственный человек'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='type_of_hike',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kapterka_app.typeofhike', verbose_name='Вид туризма'),
        ),
    ]
