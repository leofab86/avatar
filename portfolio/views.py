from django.http import JsonResponse
from portfolio.models import ProjectDetails
from portfolio.serializers import ProjectDetailsSerializer
from reactserver.views import react_render


def home(request):
    json_request = request.GET.get('json', 'false')
    try:
        projects = ProjectDetailsSerializer(ProjectDetails.objects.all(), many=True).data
    except ProjectDetails.DoesNotExist:
        projects = []

    content = {'projects': projects, 'title': 'Portfolio'}

    if json_request == 'true':
        return JsonResponse(content)

    return react_render(content, request)


def details(request, project_id):
    json_request = request.GET.get('json', 'false')
    try:
        project = ProjectDetailsSerializer(ProjectDetails.objects.get(pk=project_id)).data
    except ProjectDetails.DoesNotExist:
        project = None

    title = project['project_name'] if project is not None else 'Project not found'
    content = {'project': project, 'title': title}

    if json_request == 'true':
        return JsonResponse(content)

    return react_render(content, request)


