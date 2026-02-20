
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class PostManager(models.Manager):

    def published(self):
        return self.filter(is_published=True)

    def recent(self):
        return self.filter(created_at__gte=timezone.now()-timezone.timedelta(days=7))

    def with_comments(self):
        return self.filter(comments__isnull=False).distinct()


class CommentManager(models.Manager):

    def for_post(self, post):
        return self.filter(
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id
        )

    def recent(self):
        return self.filter(
            created_at__gte=timezone.now()-timezone.timedelta(hours=24)
        )


class Author(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    images = GenericRelation('Image')

    def __str__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    comments = GenericRelation('Comment')
    images = GenericRelation('Image')

    objects = PostManager()

    def __str__(self):
        return self.title


class Comment(models.Model):

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey()

    objects = CommentManager()


class Image(models.Model):

    url = models.URLField()
    description = models.CharField(max_length=255)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey()
