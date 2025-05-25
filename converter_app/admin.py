from django.contrib import admin
from .models import EmailUsers, Newsletter


# Register your models here.
admin.site.register(EmailUsers)
admin.site.register(Newsletter)

