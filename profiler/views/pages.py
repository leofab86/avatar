import json
from profiler.models import DatabaseProfile, Class
from profiler.serializers import DatabaseProfileSerializer
from reactserver.views import HybridJsonView
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponseRedirect


class IndexView(HybridJsonView):
    def get_content(self, request):
        try:
            db_profiles = DatabaseProfile.objects.filter(completion_progress=100)

        except DatabaseProfile.DoesNotExist:
            db_profiles = []

        serializer = DatabaseProfileSerializer(db_profiles, many=True)

        return {'db_profiles': serializer.data, 'title': 'Profiler'}


class LoadTestSSRPreview(HybridJsonView):
    def get_content(self, request):
        data_size = request.GET.get('data_size', 'none')
        with_api = request.GET.get('with_api', 'false')
        json_request = request.GET.get('json', 'false')

        content = {
            'title': 'Load Test Preview',
            'static_context': {
                'query_params': {'data_size': data_size, 'with_api': with_api}
            }
        }

        if with_api == 'false' or json_request == 'true':
            content.update(_get_preview_data(data_size))

        return content


class LoadTestSPAPreview(TemplateView):
    template_name = 'reactserver/react-spa.html'

    def get_context_data(self):
        return {'title': 'Load Test Preview', 'data': json.dumps({"spa": True})}

    def get(self, request, *args, **kwargs):
        json_request = request.GET.get('json', 'false')
        data_size = request.GET.get('data_size', 'none')
        with_api = request.GET.get('with_api', 'true')

        if json_request == 'true':
            context = self.get_context_data()
            context.update(_get_preview_data(data_size))
            return JsonResponse(context)

        if with_api == 'false':
            return HttpResponseRedirect(f'/profiler/preview/spa?data_size={data_size}&with_api=true')

        return super().get(self, request, *args, **kwargs)


def _get_preview_data(data_size):
    db_profiles = []
    classes = []

    if data_size == 'small':
        try:
            db_profiles = DatabaseProfile.objects.filter(completion_progress=100)
            db_profiles = DatabaseProfileSerializer(db_profiles, many=True).data

        except DatabaseProfile.DoesNotExist:
            db_profiles = []

    if data_size == 'large':
        try:
            classes = Class.objects.all()
            classes = [c.serialize() for c in classes]
        except Class.DoesNotExist:
            classes = []

    return {'db_profiles': db_profiles, 'classes': classes}