# -*- coding: utf-8 -*-
import os
import string
from random import Random

from django.conf import settings

from django.core.management.base import BaseCommand

from core.models import User
from publications.models import Publication

# from publications.models import Publication

publication_types = ["news", "achievement"]


class Command(BaseCommand):
    help = "Manipulations with publications (add, show, delete)"

    def add_arguments(self, parser):
        parser.add_argument("n", nargs='?', type=int, default=1)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--delete', "-d", action='store_true', help="Delete all publications from db")
        group.add_argument('--add', "-a", action='store_true',
                           help="Add new publications to random users (in number of n) to db")
        group.add_argument('--show', "-s", action='store_true', help="Show publications of users in db")

    def handle(self, *args, **options):
        print(options)
        if options['delete']:
            self.delete_publications()
        elif options['show']:
            self.show_publications()
        elif options['add']:
            self.add_publications(options['n'])

        self.stdout.write("Done!")

    def delete_publications(self):
        self.stdout.write("Deleting all publications from database")
        publications_number = Publication.objects.all().count()
        self.stdout.write("Deleted publications: %i" % publications_number)
        User.objects.all().delete()

    def show_publications(self):
        self.stdout.write("Showing all publications in database")
        users = User.objects.all()
        publications = Publication.objects.all()
        total_publications = publications.count()
        if total_publications > 0:
            self.stdout.write("Total publications: %i)" % total_publications)
            for user in users:
                self.stdout.write(
                    "%s, publications: %i" % (user.full_name, publications.filter(author=user.id).count()))
        else:
            self.stdout.write("No user with publication in database")

    def add_publications(self, number):
        if number > 0:
            random = Random()
            users = User.objects.all()
            charts = string.lowercase + " "
            for i in range(number):
                content = "".join([random.choice(charts) for a in range(random.randint(40, 100))])
                publication_title = "".join(
                    [random.choice(string.lowercase) for a in range(random.randint(15, 30))]).title()
                author = random.choice(users)
                publication_type = random.choice(publication_types)
                publication = Publication(author=author, title=publication_title, content=content,
                                          publication_type=publication_type)
                publication.save()
            self.stdout.write("%i publications was added to database" % number)
        else:
            self.stdout.write("Invalid number of publications to add was set. Nothing done")
