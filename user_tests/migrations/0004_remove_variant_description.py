# Generated by Django 3.2 on 2021-11-15 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_tests', '0003_auto_20211115_0208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='description',
        ),
    ]
