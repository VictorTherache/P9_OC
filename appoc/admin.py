from django.contrib import admin

# Register your models here.
from .models import Review, Ticket, UserFollows

admin.site.register(Review)
admin.site.register(Ticket)
admin.site.register(UserFollows)
