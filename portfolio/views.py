from portfolio.models import ProjectDetails
from reactserver.views import HybridJsonView
from portfolio.serializers import ProjectDetailsSerializer


class HomeView(HybridJsonView):
    def get_content(self, request):
        try:
            projects = ProjectDetailsSerializer(ProjectDetails.objects.all(), many=True).data
        except ProjectDetails.DoesNotExist:
            projects = []

        return {'projects': projects, 'title': 'Portfolio'}


class DetailsView(HybridJsonView):
    def get_content(self, request, project_id):
        try:
            project = ProjectDetailsSerializer(ProjectDetails.objects.get(pk=project_id)).data
        except ProjectDetails.DoesNotExist:
            project = None

        title = project['project_name'] if project is not None else 'Project not found'
        return {'project': project, 'title': title}
