import csv

from django.core.management.base import BaseCommand

from home.models import Book

class Command(BaseCommand):
    '''customize command to create new books from csv file'''
    help = "import new books from the csv file"

    def add_arguments(self, parser):
        '''method to read and add command line arguments'''
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        '''method to create new users by reading data from csv file'''
        csv_file = kwargs['csv_file']

        books_to_create = []

        with open(csv_file, encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                book = Book(
                    name=row['name'],
                    author_name=row['author'],
                    publisher_name=row['publisher'],
                    number_of_books=int(row['number of books'])
                )
                books_to_create.append(book)

        Book.objects.bulk_create(books_to_create)

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(books_to_create)} books'))
