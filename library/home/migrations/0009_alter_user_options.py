# Generated by Django 4.2.4 on 2023-08-21 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
