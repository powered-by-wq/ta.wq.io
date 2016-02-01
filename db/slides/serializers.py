from rest_framework import serializers
from wq.db.rest.serializers import ModelSerializer
from django.conf import settings

class NextSlideSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField(source='slug')
    transition = serializers.ReadOnlyField()
    icon = serializers.SerializerMethodField()
    image = serializers.FileField()
    
    def get_icon(self, instance):
        if 'up' in instance.transition:
            return 'arrow-d'
        elif 'down' in instance.transition:
            return 'arrow-u'
        return 'arrow-r'

class PreviousSlideSerializer(NextSlideSerializer):
    transition = serializers.SerializerMethodField()
    def get_transition(self, instance):
        return instance.next.transition

    def get_icon(self, instance):
        current = instance.next
        if 'up' in current.transition:
            return 'arrow-u'
        elif 'down' in current.transition:
            return 'arrow-d'
        return 'arrow-l'

class PresentationSerializer(ModelSerializer):
    first = NextSlideSerializer()

class SlideSerializer(ModelSerializer):
    previous = PreviousSlideSerializer()
    next = NextSlideSerializer()
    markdown_parts = serializers.SerializerMethodField()

    def get_markdown_parts(self, instance):
        parts = instance.markdown and instance.markdown.split('\r\n--\r\n')
        if parts and len(parts) > 1:
            return parts

    html = serializers.SerializerMethodField()
    def get_html(self, instance):
        from markdown import markdown
        extensions = getattr(settings, 'MARKDOWN_EXTENSIONS', [])
        parts = self.get_markdown_parts(instance)
        if parts:
            step = int(self.context['request'].GET.get('step', 0))
            if step >= len(parts):
                step = -2
            md = '\r\n'.join(parts[0:step+1])
        else:
            md = instance.markdown
        return markdown(md, extensions)

    class Meta:
        list_exclude = ['html']
