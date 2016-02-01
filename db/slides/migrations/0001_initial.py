# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('affiliation', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(blank=True, null=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('delay', models.IntegerField(default=0)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('presentation', models.ForeignKey(to='slides.Presentation')),
            ],
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, null=True, max_length=255)),
                ('menu_name', models.CharField(blank=True, null=True, max_length=255)),
                ('transition', models.CharField(max_length=10, choices=[('fade', 'Fade In'), ('pop', 'Pop'), ('flip', 'Flip'), ('turn', 'Turn'), ('flow', 'Flow'), ('slidefade', 'Slide+Fade'), ('slide', 'Slide Across'), ('slideup', 'Slide Up'), ('slidedown', 'Slide Down'), ('none', 'No Transition')])),
                ('markdown', models.TextField(blank=True, null=True)),
                ('html', models.TextField(blank=True, null=True)),
                ('url', models.CharField(blank=True, null=True, max_length=255)),
                ('image', models.ImageField(upload_to='slides', blank=True, null=True)),
                ('image_mode', models.CharField(default='fade', max_length=10, choices=[('fade', 'Fade In'), ('pop', 'Pop'), ('flip', 'Flip'), ('turn', 'Turn'), ('flow', 'Flow'), ('slidefade', 'Slide+Fade'), ('slide', 'Slide Across'), ('slideup', 'Slide Up'), ('slidedown', 'Slide Down'), ('none', 'No Transition')])),
                ('script', models.ForeignKey(to='slides.Script', null=True, blank=True)),
                ('section', models.ForeignKey(to='slides.Section')),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('content', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='slide',
            name='style',
            field=models.ForeignKey(to='slides.Style', null=True, blank=True),
        ),
        migrations.AlterOrderWithRespectTo(
            name='slide',
            order_with_respect_to='section',
        ),
        migrations.AlterOrderWithRespectTo(
            name='section',
            order_with_respect_to='presentation',
        ),
        migrations.AddField(
            model_name='presentation',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presentation',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='image_mode',
            field=models.CharField(default='height', max_length=10, choices=[('height', 'Full Height'), ('width', 'Full Width')]),
        ),
        migrations.AddField(
            model_name='slide',
            name='presentation',
            field=models.ForeignKey(to='slides.Presentation', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slide',
            name='slug',
            field=models.SlugField(default='first'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='slide',
            name='html',
        ),
        migrations.AddField(
            model_name='slide',
            name='zoom',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='presentation',
            name='markdown',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='markdown',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='slide',
            name='width',
            field=models.FloatField(default=1024.0),
        ),
        migrations.AddField(
            model_name='slide',
            name='mobile',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='slide',
            name='left',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='slide',
            name='top',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='section',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterOrderWithRespectTo(
            name='section',
            order_with_respect_to=None,
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['presentation', 'position']},
        ),
        migrations.AddField(
            model_name='slide',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='slide',
            options={'ordering': ['presentation', 'section__position', 'position']},
        ),
        migrations.AddField(
            model_name='slide',
            name='lock_zoom',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterOrderWithRespectTo(
            name='slide',
            order_with_respect_to=None,
        ),
        migrations.AddField(
            model_name='presentation',
            name='authors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='presentation',
            name='image',
            field=models.ImageField(upload_to='', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='slide',
            name='transition',
            field=models.CharField(default='slide', max_length=10, choices=[('slide', 'Slide Across'), ('none', 'No Transition'), ('flow', 'Flow'), ('flip', 'Flip'), ('slideup', 'Slide Up'), ('slidedown', 'Slide Down'), ('fade', 'Fade In'), ('slidefade', 'Slide Out, Fade In'), ('pop', 'Pop'), ('turn', 'Turn')]),
        ),
    ]
