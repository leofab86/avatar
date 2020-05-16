from django.contrib import admin

from .models import ProjectDetails


class ProjectDetailsAdmin(admin.ModelAdmin):
    list_display = ['project_name']


admin.site.register(ProjectDetails, ProjectDetailsAdmin)
