from django.contrib import admin

from .models import Category, Item, Tag


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "is_published"]
    list_editable = ["is_published"]
    list_display_links = ["name"]
    filter_horizontal = ["tags"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
