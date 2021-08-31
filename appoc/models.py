from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.db.models.fields.related import ForeignKey


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    # Your Ticket model definition goes here


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket,
                               on_delete=models.CASCADE,
                               default="",
                               related_name="reviews")
    note = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    titre = models.CharField(max_length=128, default="")
    commentaire = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = ForeignKey(to=settings.AUTH_USER_MODEL,
                      on_delete=models.CASCADE,
                      related_name='following')
    followed_user = ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')
