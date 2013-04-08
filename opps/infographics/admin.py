# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import (Infographic, InfographicPost, InfographicBox,
                     InfographicBoxInfographics, InfographicConfig,
                     InfographicItem, InfographicTimeline,
                     InfographicTimelineSlide, InfographicInfographicItem)

from opps.core.admin import PublishableAdmin

from redactor.widgets import RedactorEditor


class InfographicAdminForm(forms.ModelForm):
    class Meta:
        model = Infographic
        widgets = {"headline": RedactorEditor(),
                   "description": RedactorEditor()}


class InfographicItemForm(forms.ModelForm):
    class Meta:
        model = InfographicItem
        widgets = {"description": RedactorEditor()}


class InfographicPostInline(admin.TabularInline):
    model = InfographicPost
    fk_name = 'infographic'
    raw_id_fields = ['post']
    actions = None
    extra = 1
    classes = ('collapse',)


class InfographicItemInline(admin.TabularInline):
    model = InfographicInfographicItem
    fk_name = 'infographic'
    raw_id_fields = ['item']
    actions = None
    extra = 1
    classes = ('collapse',)


class InfographicAdmin(PublishableAdmin):
    form = InfographicAdminForm
    prepopulated_fields = {"slug": ["title"]}
    list_display = ['title', 'channel', 'type', 'date_available', 'published']
    list_filter = ["date_available", "published", "channel"]
    search_fields = ["title", "headline", "description"]
    exclude = ('user',)
    raw_id_fields = ['main_image', 'top_image', 'channel', 'timeline']
    inlines = [InfographicPostInline, InfographicItemInline]

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('title', 'slug')}),
        (_(u'Headline'), {
            'fields': ('headline', 'main_image', 'top_image', 'tags')}),
        (_(u'Description'), {
            'fields': ('description',)}),
        (_(u'Relationships'), {
            'fields': ('channel', 'timeline')}),
        (_(u'Config'), {
            'fields': ('type', 'css_path', 'js_path')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available', 'order')}),
    )


class InfographicItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ('image', 'album')
    list_display = ('title', 'group', 'order')
    list_filter = ('group', 'infographic_item')
    list_editable = ('order',)
    form = InfographicItemForm


class InfographicTimelineSlideInline(admin.StackedInline):
    model = InfographicTimelineSlide
    fk_name = 'timeline'
    # raw_id_fields = ['item']
    actions = None
    extra = 1
    classes = ('collapse',)

    fieldsets = [
        (_(u"Basic"), {'fields': ('type', 'headline', 'text')}),
        (_(u"Config"), {
            'fields': (
                ('start_date', 'end_date'),
                ('tag', 'value'),
                ('classname', 'order'),
            )
        }),
        (_(u"Media"), {
            'fields': (
                ('media', 'thumbnail'),
                ('caption', 'credit'),
            )
        })
    ]


class InfographicTimelineAdmin(admin.ModelAdmin):
    inlines = (InfographicTimelineSlideInline,)
    fieldsets = [
        (_(u"Basic"), {'fields': ('title', 'json', 'source')}),
        (_(u"Config"), {
            'fields': (
                ('type', 'embed_id', 'lang'),
                ('width', 'height'),
                ('start_at_end', 'hash_bookmark', 'debug'),
                ('start_at_slide', 'start_zoom_adjust'),
                ('maptype', 'gmap_key'),
                'font',
            )
        })
    ]


class InfographicTimelineSlideAdmin(admin.ModelAdmin):
    raw_id_fields = ('timeline',)
    fieldsets = [
        (_(u"Basic"), {'fields': ('type', 'headline', 'text')}),
        (_(u"Config"), {
            'fields': (
                ('start_date', 'end_date'),
                ('tag', 'value'),
                ('classname', 'order'),
            )
        }),
        (_(u"Media"), {
            'fields': (
                ('media', 'thumbnail'),
                ('caption', 'credit'),
            )
        })
    ]


class InfographicBoxInfographicsInline(admin.TabularInline):
    model = InfographicBoxInfographics
    fk_name = 'infographicbox'
    raw_id_fields = ['infographic']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('infographic', 'order')})]


class InfographicBoxAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    inlines = [InfographicBoxInfographicsInline]
    exclude = ('user',)
    raw_id_fields = ['channel', 'article']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'article')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class InfographicConfigAdmin(PublishableAdmin):
    list_display = ['key', 'key_group', 'channel', 'date_insert',
                    'date_available', 'published']
    list_filter = ["key", 'key_group', "channel", "published"]
    search_fields = ["key", "key_group", "value"]
    raw_id_fields = ['infographic', 'channel', 'article']
    exclude = ('user',)


admin.site.register(Infographic, InfographicAdmin)
admin.site.register(InfographicBox, InfographicBoxAdmin)
admin.site.register(InfographicConfig, InfographicConfigAdmin)
admin.site.register(InfographicItem, InfographicItemAdmin)
admin.site.register(InfographicTimeline, InfographicTimelineAdmin)
admin.site.register(InfographicTimelineSlide, InfographicTimelineSlideAdmin)
