# -*- coding: utf-8 -*-
import os
import string
from random import Random

from django.conf import settings

from django.core.management.base import BaseCommand

from core.models import User

# first_names = [u"Илья", u"Вадим", u"Дмитрий", u"Александр", u"Олег", u"Игорь", u"Антон"]
# last_names = [u"Иванов", u"Петров", u"Сидоров", u"Кротов", u"Соколов", u"Смирнов"]
first_names = ["Alexandr", "Egor", "Philip", "Jenny", "Ada", "John", "Peter"]
last_names = ["Smith", "Schwarz", "Komplihn", "Franklin", "Potter"]


class Command(BaseCommand):
    help = "Manipulations with users (add, show, delete)"

    def add_arguments(self, parser):
        parser.add_argument("n", nargs='?', type=int, default=1)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--delete', "-d", action='store_true', help="Delete all users from db")
        group.add_argument('--add', "-a", action='store_true', help="Add new users (in number of n) to db")
        group.add_argument('--show', "-s", action='store_true', help="Show all users in db")

    def handle(self, *args, **options):
        # print(options)
        if options['delete']:
            self.delete_users()
        elif options['show']:
            self.show_users()
        elif options['add']:
            self.add_users(options['n'])

        self.stdout.write("Done!")

    def delete_users(self):
        self.stdout.write("Deleting all users from database")
        users_number = User.objects.all().count()
        self.stdout.write("Deleted users: %i" % users_number)
        User.objects.all().delete()

    def show_users(self):
        self.stdout.write("Showing all users in database")
        users = User.objects.all()
        total_users = users.count()
        if total_users > 0:
            self.stdout.write("List of users (total %i)" % total_users)
            for i in range(total_users):
                self.stdout.write(
                    "%i. %s, %s (%s)" % (i + 1, users[i].first_name, users[i].last_name, users[i].username))
        else:
            self.stdout.write("No user in database")

    def add_users(self, number):
        if number > 0:
            random = Random()
            for i in range(number):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                username = "@" + "".join([random.choice(string.lowercase) for a in range(random.randint(10,20))])
                user = User(username=username, first_name=first_name, last_name=last_name)
                user.save()
            self.stdout.write("%i users was added to database" % number)
        else:
            self.stdout.write("Invalid number of users to add was set. Nothing done")
