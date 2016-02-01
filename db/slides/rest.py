from wq.db import rest

from .models import Presentation, Section, Slide, Script, Style
from .serializers import PresentationSerializer, SlideSerializer
from .views import SlideViewSet

rest.router.register_model(
    Presentation,
    serializer=PresentationSerializer,
    url='',
    lookup='slug',
)
rest.router.register_model(Section)
rest.router.register_model(
    Slide,
    queryset=Slide.objects.order_by('section__presentation', 'section__position', 'position'),
    serializer=SlideSerializer,
    viewset=SlideViewSet,
    lookup='slug',
    per_page=10000,
)
rest.router.register_model(Script)
rest.router.register_model(Style)
rest.router.add_page('menu', {'url': 'menu'})
