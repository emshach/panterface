# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-29 18:36
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import friede.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('path', models.CharField(max_length=255)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActionEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Action')),
            ],
            options={
                'verbose_name_plural': 'action entries',
            },
        ),
        migrations.CreateModel(
            name='AppEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
            ],
            options={
                'verbose_name_plural': 'app entries',
            },
        ),
        migrations.CreateModel(
            name='BlockEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
            ],
            options={
                'verbose_name_plural': 'block entries',
            },
        ),
        migrations.CreateModel(
            name='ContainerEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
            ],
            options={
                'verbose_name_plural': 'container entries',
            },
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('path', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IconEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Icon')),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'verbose_name_plural': 'icon entries',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('path', models.CharField(max_length=255)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LinkEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Link')),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'verbose_name_plural': 'link entries',
            },
        ),
        migrations.CreateModel(
            name='LocationEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'verbose_name_plural': 'location entries',
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('path', models.CharField(max_length=255)),
                ('target', models.CharField(max_length=255)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReferenceEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Reference')),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'verbose_name_plural': 'reference entries',
            },
        ),
        migrations.CreateModel(
            name='Registry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('path', models.CharField(max_length=255)),
                ('format', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('default', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScreenEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'verbose_name_plural': 'screen entries',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('path', models.CharField(max_length=255)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('type', models.CharField(choices=[('BooleanField', 'True/False'), ('CharField', 'String'), ('ChoiceField', 'Choice'), ('TypedChoiceField', 'Choice (typed)'), ('DateField', 'Date'), ('DateTimeField', 'Date and time'), ('DecimalField', 'Decibal'), ('DurationField', 'Duration'), ('EmailField', 'Email'), ('FileField', 'File'), ('FilePathField', 'File-path'), ('FloatField', 'Fraction'), ('ImageField', 'Image'), ('IntegerField', 'Integer'), ('GenericIPAddressField', 'IP Address'), ('MultipleChoiceField', 'Multiple Choice'), ('TypedMultipleChoiceField', 'Multiple Choice (typed)'), ('NullBooleanField', 'True/False/Null'), ('RegexField', 'Regular Expression'), ('SlugField', 'Slug'), ('TimeField', 'Time'), ('URLField', 'URL'), ('UUIDField', 'UUID'), ('ComboField', 'Combo'), ('MultiValueField', 'Multiple Values'), ('SplitDateTimeField', 'Split date and time'), ('ModelChoiceField', 'Model Choice'), ('ModelMultipleChoiceField', 'Multiple Model Choice')], default='CharField', max_length=32)),
                ('default', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('extends', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='exdended_by', to='friede.Setting')),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SettingEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Setting')),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'verbose_name_plural': 'setting entries',
            },
        ),
        migrations.CreateModel(
            name='ShellEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'verbose_name_plural': 'shell entries',
            },
        ),
        migrations.CreateModel(
            name='SlotEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'verbose_name_plural': 'slot entries',
            },
        ),
        migrations.CreateModel(
            name='ThemeEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'verbose_name_plural': 'theme entries',
            },
        ),
        migrations.CreateModel(
            name='WidgetEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('position', models.PositiveSmallIntegerField(default=friede.models._get_entry_position)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon')),
            ],
            options={
                'verbose_name_plural': 'widget entries',
            },
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('registry_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_app', serialize=False, to='friede.Registry')),
                ('module', models.CharField(max_length=128)),
                ('rest', models.CharField(default=True, max_length=32)),
                ('version', models.CharField(default='0.0.0', max_length=32)),
                ('available', models.CharField(default='0.0.0', max_length=32)),
            ],
            options={
                'abstract': False,
            },
            bases=('friede.registry', models.Model),
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('min_x', models.PositiveSmallIntegerField(default=1)),
                ('max_x', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('min_y', models.PositiveSmallIntegerField(default=1)),
                ('max_y', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('registry_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_block', serialize=False, to='friede.Registry')),
                ('extends', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='exdended_by', to='friede.Block')),
            ],
            options={
                'abstract': False,
            },
            bases=('friede.registry', models.Model),
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('registry_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_container', serialize=False, to='friede.Registry')),
            ],
            options={
                'abstract': False,
            },
            bases=('friede.registry',),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('registry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='friede.Registry')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('href', models.CharField(default='#', max_length=255)),
                ('app', models.ForeignKey(null=True,blank=True,on_delete=django.db.models.deletion.CASCADE, to='friede.App')),
                ('redirect_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='redirect_from', to='friede.Location')),
            ],
            options={
                'abstract': False,
            },
            bases=('friede.registry', models.Model),
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('min_x', models.PositiveSmallIntegerField(default=1)),
                ('max_x', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('min_y', models.PositiveSmallIntegerField(default=1)),
                ('max_y', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('registry_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_screen', serialize=False, to='friede.Registry')),
                ('extends', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='exdended_by', to='friede.Screen')),
            ],
            options={
                'abstract': False,
            },
            bases=('friede.registry', models.Model),
        ),
        migrations.CreateModel(
            name='Shell',
            fields=[
                ('registry_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_shell', serialize=False, to='friede.Registry')),
                ('templates', models.CharField(max_length=255)),
                ('template', models.CharField(default='index.html', max_length=255)),
                ('extends', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='exdended_by', to='friede.Shell')),
            ],
            options={
                'abstract': False,
            },
            bases=('friede.registry', models.Model),
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('registry_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_slot', serialize=False, to='friede.Registry')),
            ],
            options={
                'abstract': False,
            },
            bases=('friede.registry',),
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('registry_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_theme', serialize=False, to='friede.Registry')),
                ('templates', models.CharField(max_length=255)),
                ('template', models.CharField(default='index.html', max_length=255)),
                ('extends', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='exdended_by', to='friede.Theme')),
            ],
            options={
                'abstract': False,
            },
            bases=('friede.registry', models.Model),
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('min_x', models.PositiveSmallIntegerField(default=1)),
                ('max_x', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('min_y', models.PositiveSmallIntegerField(default=1)),
                ('max_y', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('registry_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_widget', serialize=False, to='friede.Registry')),
                ('extends', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='exdended_by', to='friede.Widget')),
            ],
            options={
                'abstract': False,
            },
            bases=('friede.registry', models.Model),
        ),
        migrations.AddField(
            model_name='widgetentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_widget_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='themeentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_theme_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='slotentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_slot_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='shellentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_shell_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='settingentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_setting_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='setting',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_setting_elements', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='setting',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_settings', through='friede.SettingEntry', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='screenentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_screen_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='registry',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon'),
        ),
        migrations.AddField(
            model_name='registry',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_elements', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='referenceentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_reference_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='reference',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_registry_elements', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='reference',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_references', through='friede.ReferenceEntry', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='locationentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_location_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='linkentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_link_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='link',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_link_elements', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='link',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='links', through='friede.LinkEntry', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='iconentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_icon_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='icon',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_icon_elements', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='icon',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_icons', through='friede.LocationEntry', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='containerentry',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon'),
        ),
        migrations.AddField(
            model_name='containerentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_container_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='blockentry',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon'),
        ),
        migrations.AddField(
            model_name='blockentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_block_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='appentry',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon'),
        ),
        migrations.AddField(
            model_name='appentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_app_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='actionentry',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon'),
        ),
        migrations.AddField(
            model_name='actionentry',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_action_entries', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='action',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='friede.Icon'),
        ),
        migrations.AddField(
            model_name='action',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_action_elements', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='action',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_actions', through='friede.ActionEntry', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='widgetentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Widget'),
        ),
        migrations.AddField(
            model_name='widget',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_widgets', through='friede.WidgetEntry', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='themeentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Theme'),
        ),
        migrations.AddField(
            model_name='theme',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_themes', through='friede.ThemeEntry', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='slotentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Slot'),
        ),
        migrations.AddField(
            model_name='slot',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_slots', through='friede.SlotEntry', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='shellentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Shell'),
        ),
        migrations.AddField(
            model_name='shell',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_shells', through='friede.ShellEntry', to='friede.Registry'),
        ),
        migrations.AlterUniqueTogether(
            name='settingentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AddField(
            model_name='screenentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Screen'),
        ),
        migrations.AddField(
            model_name='screen',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_screens', through='friede.ScreenEntry', to='friede.Registry'),
        ),
        migrations.AlterUniqueTogether(
            name='referenceentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AddField(
            model_name='locationentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Location'),
        ),
        migrations.AddField(
            model_name='location',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_locations', through='friede.LocationEntry', to='friede.Registry'),
        ),
        migrations.AlterUniqueTogether(
            name='linkentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AddField(
            model_name='link',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='_links', to='friede.Location'),
        ),
        migrations.AlterUniqueTogether(
            name='iconentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AddField(
            model_name='containerentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Container'),
        ),
        migrations.AddField(
            model_name='container',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_containers', through='friede.ContainerEntry', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='blockentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.Block'),
        ),
        migrations.AddField(
            model_name='block',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_blocks', through='friede.BlockEntry', to='friede.Registry'),
        ),
        migrations.AddField(
            model_name='appentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_entries', to='friede.App'),
        ),
        migrations.AddField(
            model_name='app',
            name='registries',
            field=models.ManyToManyField(blank=True, related_name='_apps', through='friede.AppEntry', to='friede.Registry'),
        ),
        migrations.AlterUniqueTogether(
            name='actionentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='widgetentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='themeentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='slotentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='shellentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='screenentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='locationentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='containerentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='blockentry',
            unique_together=set([('registry', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='appentry',
            unique_together=set([('registry', 'name')]),
        ),
    ]
