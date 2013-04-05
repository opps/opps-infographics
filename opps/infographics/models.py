# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from opps.core.models import Publishable, BaseBox, BaseConfig


class Infographic(Publishable):
    title = models.CharField(_(u"Title"), max_length=255)
    slug = models.SlugField(_(u"URL"), max_length=150, unique=True,
                            db_index=True)

    headline = models.TextField(_(u"Headline"), blank=True)
    description = models.TextField(_(u"Description"), blank=True)
    channel = models.ForeignKey('channels.Channel', null=True, blank=True,
                                on_delete=models.SET_NULL)
    posts = models.ManyToManyField('articles.Post', null=True, blank=True,
                                   related_name='infographic_post',
                                   through='InfographicPost')
    items = models.ManyToManyField('infographics.InfographicItem', null=True, blank=True,
                                   related_name='infographic_item',
                                   through='InfographicInfographicItem')

    top_image = models.ForeignKey('images.Image',
                                   verbose_name=_(u'Infographic Top Image'), blank=True,
                                   null=True, on_delete=models.SET_NULL,
                                   related_name='infographic_topimage')

    main_image = models.ForeignKey('images.Image',
                                   verbose_name=_(u'Infographic Image'), blank=True,
                                   null=True, on_delete=models.SET_NULL,
                                   related_name='infographic_image')

    position  = models.IntegerField(_(u"Position"), default=0)
    tags = TaggableManager(blank=True)


    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['position']


class InfographicPost(models.Model):
    post = models.ForeignKey('articles.Post', verbose_name=_(u'Infographic Post'), null=True,
                             blank=True, related_name='infographicpost_post',
                             on_delete=models.SET_NULL)
    infographic = models.ForeignKey('infographics.Infographic', verbose_name=_(u'Infographic'), null=True,
                                   blank=True, related_name='infographic',
                                   on_delete=models.SET_NULL)


    def __unicode__(self):
        return u"{0}-{1}".format(self.infographic.slug, self.post.slug)


class InfographicBox(BaseBox):

    infographics = models.ManyToManyField(
        'infographics.Infographic',
        null=True, blank=True,
        related_name='infographicbox_infographics',
        through='infographics.InfographicBoxInfographics'
    )


class InfographicBoxInfographics(models.Model):
    infographicbox = models.ForeignKey(
        'infographics.InfographicBox',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='infographicboxinfographics_infographicboxes',
        verbose_name=_(u'Infographic Box'),
    )
    infographic = models.ForeignKey(
        'infographics.Infographic',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='infographicboxinfographics_infographics',
        verbose_name=_(u'Infographic'),
    )
    order = models.PositiveIntegerField(_(u'Order'), default=0)

    def __unicode__(self):
        return u"{0}-{1}".format(self.infographicbox.slug, self.infographic.slug)

    def clean(self):

        if not self.infographic.published:
            raise ValidationError(_(u'Infographic not published!'))

        if not self.infographic.date_available <= timezone.now():
            raise ValidationError(_(u'Infographic date_available is greater than today!'))


class InfographicConfig(BaseConfig):

    infographic = models.ForeignKey(
        'infographics.Infographic',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='infographicconfig_infographics',
        verbose_name=_(u'Infographic'),
    )

    class Meta:
        permissions = (("developer", "Developer"),)
        unique_together = ("key_group", "key", "site", "channel", "article", "infographic")

