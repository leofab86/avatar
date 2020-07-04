import requests
from django.conf import settings
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from common.errorhandling import generate_error_page
from common.logging import logerror, timing


class HybridJsonView(View):
    def get_content(self, *args, **kwargs):
        return {}

    @timing('profiler')
    def get(self, request, *args, timer, **kwargs):
        with timer.run('get-content'):
            json_request = request.GET.get('json', 'false')

            content = self.get_content(request, *args, **kwargs)

            if json_request == 'true':
                return JsonResponse(content)

            render_assets = {
                'path': request.path_info
            }

            render_assets.update(content)

        with timer.run('reactserver-req'):
            try:
                res = requests.post(
                    settings.REACTSERVER_URL + '/render-react',
                    json=render_assets,
                    headers={'content_type': 'application/json'}
                )

            except Exception as e:
                logerror(e, message='react_render failed to communicate with Reactserver')
                return generate_error_page(
                    request,
                    code='REACTSERVER_ERROR',
                    message='There was a problem communicating with the react server',
                    status=500,
                )

        with timer.run('generate-response'):
            context = res.json()
            content = loader.render_to_string('reactserver/react-spa.html', context, request)
            response = HttpResponse(content)

        response['Server-Timing'] = res.headers['Server-Timing']

        if not settings.DEBUG:
            try:
                response['Instance-Id'] = requests.get('http://169.254.169.254/latest/meta-data/instance-id').text
            except:
                '''do nothing'''

        return response
