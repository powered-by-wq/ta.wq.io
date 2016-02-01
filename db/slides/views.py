from wq.db.rest.views import ModelViewSet
from rest_framework.decorators import detail_route


class SlideViewSet(ModelViewSet):
    ignore_kwargs = ['step']
    @detail_route(methods=['post'])
    def zoom(self, request, *args, **kwargs):
        result = super().retrieve(request, *args, **kwargs)
        obj = self.get_object()
        if obj.lock_zoom:
            return result
        for field in ('zoom', 'width', 'left', 'top'):
            if field in request.POST:
                setattr(obj, field, request.POST[field])
        obj.save()
        return result
