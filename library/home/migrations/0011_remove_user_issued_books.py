# Generated by Django 4.2.4 on 2023-08-21 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_user_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='issued_books',
        ),
    ]