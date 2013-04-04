# -*- coding: utf-8 -*-
from django import template
from opps.infographics.models import Infographic, InfographicBox

register = template.Library()

@register.simple_tag
def get_all_infographics(number=5, channel_slug=None,
                template_name='infographics/actives.html'):

    active_infographics = Infographic.objects.all_published()
    if channel_slug:
        active_infographics = active_infographics.filter(channel__slug=channel_slug)

    active_infographics = active_infographics[:number]

    t = template.loader.get_template(template_name)

    return t.render(template.Context({'active_infographics': active_infographics,
                                      'channel_slug': channel_slug,
                                      'number': number}))

@register.simple_tag
def get_infographicbox(slug, channel_slug=None, template_name=None):
    if channel_slug:
        slug = u"{0}-{1}".format(slug, channel_slug)

    try:
        box = InfographicBox.objects.get(site=settings.SITE_ID, slug=slug,
                                     date_available__lte=timezone.now(),
                                     published=True)
    except InfographicBox.DoesNotExist:
        box = None

    t = template.loader.get_template('infographics/infographicbox_detail.html')
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({'infographicbox': box, 'slug': slug}))


@register.simple_tag
def get_all_infographicbox(channel_slug, template_name=None):
    boxes = InfographicBox.objects.filter(site=settings.SITE_ID,
                                      date_available__lte=timezone.now(),
                                      published=True,
                                      channel__slug=channel_slug)

    t = template.loader.get_template('infographics/infographicbox_list.html')
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({'infographicboxes': boxes}))
