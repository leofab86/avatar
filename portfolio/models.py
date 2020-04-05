from django.db import models


class Test(models.Model):
    text_prop1 = models.CharField(max_length=200)

    def __str__(self):
        return self.text_prop1


class ProjectDetails(models.Model):
    project_name = models.CharField(max_length=200)
    project_summary = models.TextField()
    project_description = models.TextField()

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = "Project DetailsPage"
        verbose_name_plural = "Project DetailsPage"
