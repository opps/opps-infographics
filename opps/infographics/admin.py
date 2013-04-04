# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from .models import (Infographic, InfographicPost, InfographicBox,
                    InfographicBoxInfographics, InfographicConfig)

from opps.core.admin import PublishableAdmin

from redactor.widgets import RedactorEditor


class InfographicAdminForm(forms.ModelForm):
    class Meta:
        model = Infographic
        widgets = {"headline": RedactorEditor(), "description": RedactorEditor()}


class InfographicPostInline(admin.TabularInline):
    model = InfographicPost
    fk_name = 'infographic'
    raw_id_fields = ['post']
    actions = None
    extra = 1
    classes = ('collapse',)


class InfographicAdmin(PublishableAdmin):
    form = InfographicAdminForm
    prepopulated_fields = {"slug": ["title"]}
    list_display = ['title', 'channel', 'date_available', 'published']
    list_filter = ["date_available", "published", "channel"]
    search_fields = ["title", "headline", "description"]
    exclude = ('user',)
    raw_id_fields = ['main_image', 'channel']
    inlines = [InfographicPostInline]

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('title', 'slug')}),
        (_(u'Content'), {
            'fields': ('headline', 'main_image', 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available', 'position')}),
    )


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
    list_display = ['key','key_group', 'channel', 'date_insert', 'date_available', 'published']
    list_filter = ["key", 'key_group', "channel", "published"]
    search_fields = ["key", "key_group", "value"]
    raw_id_fields = ['infographic', 'channel', 'article']
    exclude = ('user',)


admin.site.register(Infographic, InfographicAdmin)
admin.site.register(InfographicBox, InfographicBoxAdmin)
admin.site.register(InfographicConfig, InfographicConfigAdmin)