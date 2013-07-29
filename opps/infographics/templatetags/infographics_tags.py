# -*- coding: utf-8 -*-

from django import template
from django.utils import timezone
from django.contrib.sites.models import get_current_site
from opps.infographics.models import Infographic, InfographicBox

register = template.Library()


@register.simple_tag(takes_context=True)
def get_all_infographics(context, number=5,
                         channel_slug=None,
                         template_name='infographics/actives.html'):

    active_infographics = Infographic.objects.all_published()
    if channel_slug:
        active_infographics = active_infographics.filter(channel__slug=channel_slug)

    active_infographics = active_infographics[:number]

    t = template.loader.get_template(template_name)

    return t.render(template.Context({'active_infographics': active_infographics,
                                      'channel_slug': channel_slug,
                                      'number': number,
                                      'context': context}))


@register.simple_tag(takes_context=True)
def get_infographicbox(context, slug, channel_slug=None, template_name=None):
    if channel_slug:
        slug = u"{0}-{1}".format(slug, channel_slug)

    site = get_current_site(context.request)

    try:
        box = InfographicBox.objects.get(
            site=site,
            slug=slug,
            date_available__lte=timezone.now(),
            published=True
        )
    except InfographicBox.DoesNotExist:
        box = None

    t = template.loader.get_template('infographics/infographicbox_detail.html')
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({'infographicbox': box,
                                      'slug': slug,
                                      'context': context}))


@register.simple_tag(takes_context=True)
def get_all_infographicbox(context, channel_slug, template_name=None):
    site = get_current_site(context.request)
    boxes = InfographicBox.objects.filter(site=site,
                                          date_available__lte=timezone.now(),
                                          published=True,
                                          channel__slug=channel_slug)

    t = template.loader.get_template('infographics/infographicbox_list.html')
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({'infographicboxes': boxes, 'context': context}))
