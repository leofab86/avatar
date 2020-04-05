import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from portfolio.models import ProjectDetails
from portfolio.serializers import ProjectDetailsSerializer


def home(request):
    json_request = request.GET.get('json', 'false')
    try:
        projects = ProjectDetailsSerializer(ProjectDetails.objects.all(), many=True).data
    except ProjectDetails.DoesNotExist:
        projects = []

    content = {'projects': projects, 'title': 'Portfolio'}

    if json_request == 'true':
        return JsonResponse(content)

    return _react_render(content, request)


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

    return _react_render(content, request)


def _react_render(content, request):
    # Let's grab our user's info if she has any
    # if request.user.is_authenticated():
    #     serializer = UserSerializer(request.user)
    #     user = serializer.data
    # else:
    #     user = {}

    # Here's what we've got so far
    render_assets = {
        'path': request.path_info
    }

    render_assets.update(content)

    try:
        res = requests.post(settings.REACTSERVER_URL + '/render-react',
                            json=render_assets,
                            headers={'content_type': 'application/json'})
        rendered_payload = res.json()
    except Exception as e:
        print('ERROR: Failed to communicate with Reactserver: ', e)
        rendered_payload = {}

    return render(request, 'portfolio/react-spa.html', rendered_payload)
