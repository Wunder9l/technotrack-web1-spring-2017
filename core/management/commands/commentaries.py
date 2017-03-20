# -*- coding: utf-8 -*-
import os
import string
from random import Random

from django.conf import settings

from django.core.management.base import BaseCommand

from core.models import User
from publications.models import Publication
from comments.models import Comment

# from publications.models import Publication

publication_types = ["news", "achievement"]


class Command(BaseCommand):
    help = "Manipulations with comments (add, show, delete)"

    def add_arguments(self, parser):
        parser.add_argument("n", nargs='?', type=int, default=1)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--delete', "-d", action='store_true', help="Delete all comments from db")
        group.add_argument('--add', "-a", action='store_true',
                           help="Add new comments to random publication (total number of comments - n) to db")
        group.add_argument('--show', "-s", action='store_true', help="Show comments of publications in db")

    def handle(self, *args, **options):
        print(options)
        if options['delete']:
            self.delete_comments()
        elif options['show']:
            self.show_comments()
        elif options['add']:
            self.add_comments(options['n'])

        self.stdout.write("Done!")

    def delete_comments(self):
        self.stdout.write("Deleting all comments from database")
        comments_number = Comment.objects.all().count()
        self.stdout.write("Deleted comments: %i" % comments_number)
        User.objects.all().delete()

    def show_comments(self):
        self.stdout.write("Showing all comments in database")
        publications = Publication.objects.all()
        comments = Comment.objects.all()
        total_comments = comments.count()
        if total_comments > 0:
            self.stdout.write("Total comments: %i)" % total_comments)
            for publication in publications:
                comments_number = comments.filter(publication=publication.id).count()
                if comments_number > 0:
                    self.stdout.write("%s, comments: %i" % (publication.title, comments_number))
        else:
            self.stdout.write("No publication with comment in database")

    def add_comments(self, number):
        if number > 0:
            random = Random()
            publications = Publication.objects.all()
            users = User.objects.all()
            charts = string.lowercase + " "
            if len(publications) > 0:
                for i in range(number):
                    content = "".join([random.choice(charts) for a in range(random.randint(20, 50))])
                    comment = Comment(publication=random.choice(publications), author=random.choice(users),
                                      content=content)
                    comment.save()
                self.stdout.write("%i comments was added to database" % number)
            else:
                self.stdout.write("No publication to add comment")
        else:
            self.stdout.write("Invalid number of comments to add was set. Nothing done")
