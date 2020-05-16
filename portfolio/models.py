from django.db import models


class ProjectDetails(models.Model):
    project_name = models.CharField(max_length=200)
    project_summary = models.TextField()
    project_description = models.TextField()

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = "Project Details Page"
        verbose_name_plural = "Project Details Page"

