# Generated by Django 4.2.4 on 2023-08-22 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_remove_user_issued_books'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]