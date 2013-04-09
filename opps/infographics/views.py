#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.utils import timezone

from opps.channels.models import Channel
from .models import Infographic

# IS THERE A BETTER WAY?
if not 'endless_pagination' in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS += (
        'endless_pagination',
    )


class InfographicList(ListView):

    context_object_name = "infographics"

    @property
    def template_name(self):

        domain_folder = 'infographics'
        if self.site.id > 1:
            domain_folder = "{0}/infographics".format(self.site)

        return '{0}/infographic_list.html'.format(domain_folder)

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        return Infographic.objects.all_published()


class ChannelInfographicList(ListView):

    context_object_name = "infographics"

    @property
    def template_name(self):
        homepage = Channel.objects.get_homepage(site=self.site)
        if not homepage:
            return None

        long_slug = self.kwargs.get('channel__long_slug',
                                    homepage.long_slug)
        if homepage.long_slug != long_slug:
            long_slug = long_slug[:-1]

        domain_folder = 'infographics'
        if self.site.id > 1:
            domain_folder = "{0}/infographics".format(self.site)

        return '{0}/{1}.html'.format(domain_folder, long_slug)

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        long_slug = self.kwargs['channel__long_slug'][:-1]
        get_object_or_404(Channel, long_slug=long_slug)
        return Infographic.objects.filter(
            channel__long_slug=long_slug,
            published=True,
            date_available__lte=timezone.now()
        )


class InfographicDetail(DetailView):

    context_object_name = "infographic"
    model = Infographic

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        names = []

        self.template_name_suffix = "{0}_{1}".format(
            self.template_name_suffix,
            self.object.type
        )

        if hasattr(self.object, '_meta'):
            app_label = self.object._meta.app_label
            object_name = self.object._meta.object_name.lower()
        elif hasattr(self, 'model') and hasattr(self.model, '_meta'):
            app_label = self.model._meta.app_label
            object_name = self.model._meta.object_name.lower()

        if self.object.channel:
            long_slug = self.object.channel.long_slug

            # site specific template folder
            # sitename/infographics/
            if self.site.id > 1:
                app_label = "{0}/{1}".format(self.site, app_label)

            # 1. try channel/infographic template
            # opps_infographic/channel-slug/infographic-slug.html
            names.append('{0}/{1}/{2}.html'.format(
                app_label, long_slug, self.kwargs['slug']
            ))
            # 2. try a generic channel template
            # opps_infographic/channel-slug/<model>_detail.html
            names.append('{0}/{1}/{2}{3}.html'.format(
                app_label, long_slug, object_name, self.template_name_suffix
            ))

        # 3. try infographic template (all channels)
        # opps_infographic/infographic-slug.html
        names.append('{0}/{1}.html'.format(
            app_label, self.kwargs['slug']
        ))

        # The least-specific option is the default <app>/<model>_detail.html;
        # only use this if the object in question is a model.
        if hasattr(self.object, '_meta'):
            names.append("%s/%s%s.html" % (
                self.object._meta.app_label,
                self.object._meta.object_name.lower(),
                self.template_name_suffix
            ))
        elif hasattr(self, 'model') and hasattr(self.model, '_meta'):
            names.append("%s/%s%s.html" % (
                self.model._meta.app_label,
                self.model._meta.object_name.lower(),
                self.template_name_suffix
            ))

        return names

    def get_object(self):
        self.site = get_current_site(self.request)
        return get_object_or_404(
            Infographic,
            slug=self.kwargs['slug'],
            published=True,
            date_available__lte=timezone.now()
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(InfographicDetail, self).get_context_data(**kwargs)

        # get item by slug
        if 'item_slug' in kwargs:
            item_slug = kwargs['item_slug']
            context['item'] = get_object_or_404(
                self.object.items,
                slug=item_slug
            )
        return self.render_to_response(context)
