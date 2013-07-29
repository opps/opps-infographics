# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import (Infographic, InfographicContainer,
                     InfographicItem, InfographicInfographicItem)

from opps.core.admin import PublishableAdmin
from opps.core.widgets import OppsEditor
from opps.core.admin import apply_opps_rules
from opps.images.generate import image_url


class InfographicAdminForm(forms.ModelForm):
    class Meta:
        model = Infographic
        widgets = {"headline": OppsEditor(),
                   "description": OppsEditor()}


class InfographicItemForm(forms.ModelForm):
    class Meta:
        model = InfographicItem
        widgets = {"description": OppsEditor()}


class InfographicContainerInline(admin.TabularInline):
    model = InfographicContainer
    fk_name = 'infographic'
    raw_id_fields = ['container']
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

    readonly_fields = ['image_thumb']

    def image_thumb(self, obj):
        if obj.item.image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.item.image.image.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True


@apply_opps_rules('infographics')
class InfographicAdmin(PublishableAdmin):
    form = InfographicAdminForm
    prepopulated_fields = {"slug": ["title"]}
    list_display = ['title', 'channel', 'type', 'date_available',
                    'published', 'preview_url']
    list_filter = ["date_available", "published", "channel"]
    search_fields = ["title", "headline", "description"]
    exclude = ('user',)
    raw_id_fields = ['main_image', 'top_image', 'channel', 'timeline']
    inlines = [InfographicContainerInline, InfographicItemInline]

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug')}),
        (_(u'Headline'), {
            'fields': ('headline', ('main_image', 'image_thumb'),
                       ('top_image', 'top_thumb'), 'tags')}),
        (_(u'Description'), {
            'fields': ('description',)}),
        (_(u'Relationships'), {
            'fields': ('channel', 'timeline')}),
        (_(u'Config'), {
            'fields': ('type', 'css_text', 'css_path', 'js_path')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available', 'order')}),
    )

    readonly_fields = ['image_thumb', 'top_thumb']

    def top_thumb(self, obj):
        if obj.top_image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.top_image.image.url, width=60, height=60))
        return _(u'No Image')
    top_thumb.short_description = _(u'Thumbnail')
    top_thumb.allow_tags = True


@apply_opps_rules('infographics')
class InfographicItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ('image', 'album', 'timeline')
    list_display = ('title', 'group', 'order', 'belongs')
    list_filter = ('group', 'infographic_item')
    list_editable = ('order',)
    ordering = ('order',)
    form = InfographicItemForm

    fieldsets = [(None,
                  {'fields':
                   ('title', 'slug', 'description', 'group',
                    ('image', 'image_thumb'), 'album', 'timeline',
                    'order', 'css_text',
                    )
                   })]

    readonly_fields = ['image_thumb']

    def image_thumb(self, obj):
        if obj.image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.image.image.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True


admin.site.register(Infographic, InfographicAdmin)
admin.site.register(InfographicItem, InfographicItemAdmin)
