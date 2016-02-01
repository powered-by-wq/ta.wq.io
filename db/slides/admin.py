from django.contrib import admin
from .models import Presentation, Section, Slide, Script, Style

class SlideAdmin(admin.ModelAdmin):
    list_filter = ['section', 'presentation']
    list_display = ['__str__', 'section', 'presentation']

class SectionInline(admin.TabularInline):
    sortable_field_name = ('position')
    exclude = ['markdown']
    model = Section

class PresentationAdmin(admin.ModelAdmin):
    inlines = [SectionInline]

class SlideInline(admin.TabularInline):
    sortable_field_name = ('position')
    fields = ['slug', 'title', 'menu_name', 'transition', 'position']
    model = Slide
    extra = 0

class SectionAdmin(admin.ModelAdmin):
    inlines = [SlideInline]
    list_filter = ['presentation']
    list_display = ['__str__', 'presentation']

admin.site.register(Presentation, PresentationAdmin)

admin.site.register(Section, SectionAdmin)
admin.site.register(Slide, SlideAdmin)
admin.site.register(Script)
admin.site.register(Style)
