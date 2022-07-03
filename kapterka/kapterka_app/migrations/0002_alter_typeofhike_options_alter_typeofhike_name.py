# Generated by Django 4.0.5 on 2022-06-17 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kapterka_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='typeofhike',
            options={'ordering': ['id'], 'verbose_name': 'Вид туризма', 'verbose_name_plural': 'Виды туризма'},
        ),
        migrations.AlterField(
            model_name='typeofhike',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Вид туризма'),
        ),
    ]
