from django.contrib import admin

from .models import Test, ProjectDetails


class TestAdmin(admin.ModelAdmin):
    ''''''


class ProjectDetailsAdmin(admin.ModelAdmin):
    list_display = ['project_name']


admin.site.register(ProjectDetails, ProjectDetailsAdmin)
admin.site.register(Test, TestAdmin)
