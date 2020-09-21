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

    @timing()
    def get(self, request, *args, timer, **kwargs):
        content = {}
        if request.user.username:
            user = {
                'username': request.user.username,
                'server_group_status': request.user.server_group_status,
                'server_group_address': request.user.server_group_address
            }
            content.update({'user': user})

        with timer.run('get-data'):
            json_request = request.GET.get('json', 'false')
            content.update(self.get_content(request, *args, **kwargs))

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
            html = loader.render_to_string('reactserver/react-spa.html', context, request)
            response = HttpResponse(html)

        response['Server-Timing'] = res.headers['Server-Timing']

        if not settings.DEBUG:
            try:
                response['Instance-Id'] = requests.get('http://169.254.169.254/latest/meta-data/instance-id').text
            except:
                '''do nothing'''

        return response
