from django.db import models


class Presentation(models.Model):
    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    markdown = models.TextField(null=True, blank=True)
    image = models.ImageField()
    authors = models.TextField(null=True, blank=True)

    @property
    def first(self):
        return self.section_set.all()[0].slide_set.all()[0]

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=255)
    presentation = models.ForeignKey(Presentation)
    markdown = models.TextField(null=True, blank=True)
    position = models.IntegerField()

    def __str__(self):
        return self.title

    def get_next_in_order(self):
        return Section.objects.get(presentation=self.presentation, position=self.position+1)
    def get_previous_in_order(self):
        return Section.objects.get(presentation=self.presentation, position=self.position-1)

    class Meta:
        ordering = ['presentation', 'position']
#        unique_together = [['presentation', 'position']]


class Author(models.Model):
    name = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Slide(models.Model):
    TRANSITION_CHOICES = (
        ('slide', 'Slide Across'),
        ('none', 'No Transition'),
        ('flow', 'Flow'),
        ('flip', 'Flip'),
        ('slideup', 'Slide Up'),
        ('slidedown', 'Slide Down'),
        ('fade', 'Fade In'),
        ('slidefade', 'Slide Out, Fade In'),
        ('pop', 'Pop'),
        ('turn', 'Turn'),
    )
    IMAGE_CHOICES = (
        ('height', 'Full Height'),
        ('width', 'Full Width'),
    )

    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=255, null=True, blank=True)
    menu_name = models.CharField(max_length=255, null=True, blank=True)
    presentation = models.ForeignKey(Presentation)
    section = models.ForeignKey(Section)
    position = models.IntegerField()

    transition = models.CharField(
        max_length=10, choices=TRANSITION_CHOICES,
        default=TRANSITION_CHOICES[0][0],
    )

    markdown = models.TextField(null=True, blank=True)
    zoom = models.FloatField(default=1.0)
    lock_zoom = models.BooleanField(default=False)
    width = models.FloatField(default=1024.0)
    left = models.FloatField(default=0)
    top = models.FloatField(default=0)
    url = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.BooleanField(default=False)

    image = models.ImageField(upload_to='slides', null=True, blank=True)
    image_mode = models.CharField(
        max_length=10,
        choices=IMAGE_CHOICES,
        default=IMAGE_CHOICES[0][0],
    )

    script = models.ForeignKey("Script", null=True, blank=True)
    style = models.ForeignKey("Style", null=True, blank=True)

    
    def __str__(self):
        return self.title or self.menu_name or "Slide %s" % self.position

    @property
    def previous(self):
        try:
            return self.get_previous_in_order()
        except Slide.DoesNotExist:
            try:
                slides = self.section.get_previous_in_order().slide_set.reverse()
                if len(slides):
                    return slides[0]
            except Section.DoesNotExist:
                return None

    def get_next_in_order(self):
        return Slide.objects.get(section=self.section, position=self.position+1)
    def get_previous_in_order(self):
        return Slide.objects.get(section=self.section, position=self.position-1)

    @property
    def next(self):
        try:
            return self.get_next_in_order()
        except Slide.DoesNotExist:
            try:
                slides = self.section.get_next_in_order().slide_set.all()
                if len(slides):
                    return slides[0]
            except Section.DoesNotExist:
                return None

    def save(self, *args, **kwargs):
        if self.section_id and not self.presentation_id:
            self.presentation_id = self.section.presentation_id
        super().save(*args, **kwargs)
      
    class Meta:
        ordering = ['presentation', 'section__position', 'position']

class Script(models.Model):
    name = models.CharField(max_length=50)
    delay = models.IntegerField(default=0)
    content = models.TextField()

    def __str__(self):
        return self.name

class Style(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.name
