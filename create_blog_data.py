
from django.core.management.base import BaseCommand
from faker import Faker
import random
from blog.models import Author, Post, Comment, Image

fake = Faker()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        authors = []

        for i in range(5):

            author = Author.objects.create(
                name=fake.name(),
                email=fake.email(),
                bio=fake.text()
            )

            authors.append(author)

            Image.objects.create(
                url=fake.image_url(),
                description="Author image",
                content_object=author
            )

        posts = []

        for i in range(20):

            post = Post.objects.create(
                title=fake.sentence(),
                content=fake.text(),
                author=random.choice(authors),
                is_published=True
            )

            posts.append(post)

            for i in range(3):

                Image.objects.create(
                    url=fake.image_url(),
                    description="Post image",
                    content_object=post
                )

        for i in range(50):

            Comment.objects.create(
                text=fake.text(),
                content_object=random.choice(posts)
            )

        print("DATA CREATED")
