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

    content = {'projects': projects, 'title': 'Profiler'}

    if json_request == 'true':
        return JsonResponse(content)

    print('WTF')
    return react_render(content, request)