# Generated by Django 4.2.4 on 2023-08-18 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_book_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='number_of_books',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
