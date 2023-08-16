'''customize managment commands classes'''
import csv

from django.core.management.base import BaseCommand

from home.models import Book

# Command to run :
# python manage.py import_books
# /Users/talha.malik/Desktop/library_project/library_management_system/books_data.csv

class Command(BaseCommand):
    '''customize command to create new books from csv file'''
    help = "import new books from the csv file"

    def add_arguments(self, parser):
        '''method to read and add command line arguments'''
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        '''method to create new users by reading data from csv file'''
        csv_file = kwargs['csv_file']

        with open(csv_file,encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                book = Book.objects.create(
                    name=row[0],
                    author_name=row[1],
                    publisher_name=row[2],
                    number_of_books=int(row[3])
                    )

                self.stdout.write(self.style.SUCCESS(f'Successfully imported book: {book}')) # pylint: disable=no-member
