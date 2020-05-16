from rest_framework.serializers import ModelSerializer
from portfolio.models import ProjectDetails


class ProjectDetailsSerializer(ModelSerializer):
    class Meta:
        model = ProjectDetails
        fields = ('id', 'project_name', 'project_summary', 'project_description')
