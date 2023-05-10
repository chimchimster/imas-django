from django.contrib import admin
from .models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'publish', 'created', 'updated', 'status')
    list_filter = ('user', 'publish', 'status')
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('title',)}