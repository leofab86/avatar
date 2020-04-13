import requests
from django.conf import settings
from django.shortcuts import render


def react_render(content, request):
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

    return render(request, 'reactserver/react-spa.html', rendered_payload)
