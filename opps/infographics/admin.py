# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .models import (Infographic, InfographicPost, InfographicBox,
                     InfographicBoxInfographics, InfographicConfig,
                     InfographicItem, InfographicInfographicItem)

from opps.core.admin import PublishableAdmin

from redactor.widgets import RedactorEditor
from opps.core.admin import apply_opps_rules


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


@apply_opps_rules('infographics')
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
            'fields': ('site', 'title', 'slug')}),
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


@apply_opps_rules('infographics')
class InfographicItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ('image', 'album', 'timeline')
    list_display = ('title', 'group', 'order', 'belongs')
    list_filter = ('group', 'infographic_item')
    list_editable = ('order',)
    ordering = ('order',)
    form = InfographicItemForm


class InfographicBoxInfographicsInline(admin.TabularInline):
    model = InfographicBoxInfographics
    fk_name = 'infographicbox'
    raw_id_fields = ['infographic']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('infographic', 'order', 'date_available', 'date_end')})]


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

    def clean_ended_entries(self, request, queryset):
        now = timezone.now()
        for box in queryset:
            ended = box.infographicboxinfographics_infographicboxes.filter(
                date_end__lt=now
            )
            if ended:
                ended.delete()
    clean_ended_entries.short_description = _(u'Clean ended infographics')

    actions = ('clean_ended_entries',)


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
# admin.site.register(InfographicTimeline, InfographicTimelineAdmin)
# admin.site.register(InfographicTimelineSlide, InfographicTimelineSlideAdmin)
