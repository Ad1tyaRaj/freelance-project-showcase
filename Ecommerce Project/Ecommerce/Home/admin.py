from django.contrib import admin
from .models import Newsletter
# Register your models here.


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)