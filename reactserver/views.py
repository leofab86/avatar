import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View


class HybridJsonView(View):
    def get_content(self, *args, **kwargs):
        return {}

    def get(self, request, *args, **kwargs):
        json_request = request.GET.get('json', 'false')

        content = self.get_content(request, *args, **kwargs)

        if json_request == 'true':
            return JsonResponse(content)

        return react_render(content, request)


def react_render(content, request):
    render_assets = {
        'path': request.path_info
    }

    render_assets.update(content)

    try:
        res = requests.post(
            settings.REACTSERVER_URL + '/render-react',
            json=render_assets,
            headers={'content_type': 'application/json'}
        )
        rendered_payload = res.json()
    except Exception as e:
        print('ERROR: Failed to communicate with Reactserver: ', e)
        rendered_payload = {}

    return render(request, 'reactserver/react-spa.html', rendered_payload)
