from django.contrib import admin

from menu.models import Menu, HeadMenu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = 'name', 'url'


@admin.register(HeadMenu)
class HeadMenuAdmin(admin.ModelAdmin):
    list_display = 'title',
