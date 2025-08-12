from django.contrib import admin
from .models import Project, Tag


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "created_at")
    list_filter = ("featured", "tags", "created_at")
    search_fields = ("title", "description", "tech_stack")
    filter_horizontal = ("tags",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
