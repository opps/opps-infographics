# -*- coding: utf-8 -*-

from jsonfield import JSONField

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from taggit.managers import TaggableManager

from opps.core.models import Publishable, BaseBox, BaseConfig


class Infographic(Publishable):

    TYPES = (
        ("gallery", _(u"Photo Gallery")),
        ("css", _(u"Custom CSS")),
        ("timeline", _(u"Timeline")),
        ("mixed", _(u"Mixed")),
    )
    title = models.CharField(_(u"Title"), max_length=255)
    slug = models.SlugField(
        _(u"URL"),
        max_length=150,
        unique=True,
        db_index=True
    )
    headline = models.TextField(_(u"Headline"), blank=True, null=True)
    description = models.TextField(
        _(u"Description"),
        blank=True,
        null=True,
        help_text=_(u'Main description, also used by timeline type')
    )
    channel = models.ForeignKey(
        'channels.Channel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    posts = models.ManyToManyField(
        'articles.Post',
        null=True,
        blank=True,
        related_name='infographic_post',
        through='InfographicPost'
    )
    top_image = models.ForeignKey(
        'images.Image',
        verbose_name=_(u'Infographic Top Image'), blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='infographic_topimage'
    )
    main_image = models.ForeignKey(
        'images.Image',
        verbose_name=_(u'Infographic Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='infographic_image'
    )

    order = models.IntegerField(_(u"Order"), default=0)
    tags = TaggableManager(blank=True)

    type = models.CharField(
        _(u"Infographic type"),
        max_length=20,
        choices=TYPES,
        default="gallery"
    )
    items = models.ManyToManyField(
        'infographics.InfographicItem',
        null=True, blank=True,
        related_name='infographic_item',
        through='InfographicInfographicItem'
    )

    # css
    css_path = models.CharField(
        _(u"Custom css path"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_(u'/static/css/file.css or http://domain.com/file.css')
    )
    #    js_filepath
    js_path = models.CharField(
        _(u"Custom Java Script path"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_(u'allowed only in the same domain')
    )

    # Timeline
    timeline = models.ForeignKey(
        'infographics.InfographicTimeline',
        verbose_name=_(u'Timeline'),
        null=True,
        blank=True,
        related_name='infographic_timeline',
        on_delete=models.SET_NULL,
        help_text=_(u'Set this and provide JSON, DOC or Items')
    )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['order']


class InfographicInfographicItem(models.Model):
    item = models.ForeignKey(
        'infographics.InfographicItem',
        verbose_name=_(u'Infographic Item'),
        null=True,
        blank=True,
        related_name='infographicitem_item',
        on_delete=models.SET_NULL
    )
    infographic = models.ForeignKey(
        'infographics.Infographic',
        verbose_name=_(u'Infographic'),
        null=True,
        blank=True,
        related_name='infographicitem_infographic',
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return u"{0}-{1}".format(self.infographic.slug, self.item.title)


class InfographicPost(models.Model):
    post = models.ForeignKey(
        'articles.Post',
        verbose_name=_(u'Infographic Post'),
        null=True,
        blank=True,
        related_name='infographicpost_post',
        on_delete=models.SET_NULL
    )
    infographic = models.ForeignKey(
        'infographics.Infographic',
        verbose_name=_(u'Infographic'),
        null=True,
        blank=True,
        related_name='infographicpost_infographic',
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return u"{0}-{1}".format(self.infographic.slug, self.post.slug)


class InfographicItem(models.Model):
    title = models.CharField(_(u"Title"), max_length=255)
    slug = models.SlugField(
        _(u"URL"),
        max_length=150,
        db_index=True
    )
    description = models.TextField(_(u"Description"), blank=True)

    # optional for gallery and css
    group = models.CharField(
        _(u"Group"),
        max_length=255,
        help_text=_(u'To group menu items or to store custom attributes')
    )

    image = models.ForeignKey(
        'images.Image',
        verbose_name=_(u'Infographic Item Image'),
        blank=True,
        null=True,
        help_text=_(u'Image'),
        on_delete=models.SET_NULL,
    )
    # gallery
    album = models.ForeignKey(
        'articles.Album',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='infographicitem_album',
        verbose_name=_(u'Album'),
    )
    order = models.IntegerField(_(u"Order"), default=0)

    __unicode__ = lambda self: self.title


class InfographicTimeline(models.Model):
    title = models.CharField(_(u"Title"), max_length=255)
    # timeline
    json = JSONField(
        _(u"Timeline Json"),
        blank=True,
        null=True,
        help_text=_(
            u'Optional JSON for timelinejs if not provided'
            u' you should add items or google spreadsheet'
        )
    )
    source = models.URLField(
        _(u"Source URL"),
        blank=True,
        null=True,
        help_text=_(
            u'Optional Google Spreadsheet or json URL for timelinejs '
            u' if not provided you should add items or json'
        )
    )

    # config
    type = models.CharField(
        _(u"Type"),
        max_length=255,
        blank=True,
        null=True,
        default='default'
    )
    width = models.CharField(
        _(u"Width"),
        max_length=5,
        blank=True,
        null=True,
        default="100%"
    )
    height = models.CharField(
        _(u"Height"),
        max_length=5,
        blank=True,
        null=True,
        default="100%"
    )
    embed_id = models.CharField(
        _(u"Embed id"),
        max_length=255,
        null=True,
        blank=True
    )
    lang = models.CharField(_(u"Title"), max_length=255, default='pt-br')
    start_at_end = models.BooleanField(default=False)
    start_at_slide = models.IntegerField(default=0)
    start_zoom_adjust = models.IntegerField(default=0)
    hash_bookmark = models.BooleanField(default=False)
    debug = models.BooleanField(default=False)
    gmap_key = models.CharField(
        _(u"Gmap Key"),
        max_length=255,
        null=True,
        blank=True
    )
    maptype = models.CharField(
        _(u"Map Type"),
        max_length=255,
        null=True,
        blank=True,
    )
    font = models.CharField(
        _(u"Font"),
        max_length=255,
        null=True,
        blank=True,
    )

    __unicode__ = lambda self: self.title


class InfographicTimelineItem(models.Model):
    # Timeline
    timeline = models.ForeignKey(
        'infographics.InfographicTimeline',
        verbose_name=_(u'Timeline'),
        null=True,
        blank=True,
        related_name='infographicitem_timeline',
        on_delete=models.SET_NULL,
    )

    type = models.CharField(
        _(u"Item type"),
        max_length=255,
        blank=True,
        null=True,
        default='date',
        help_text=_(
            u'Use "date",  "era", "title" or "chart"',
            u' Note: Only one can be "title"',
            u' and "era" displays only headline and dates'
        )
    )
    headline = models.CharField(
        _(u"Timeline Headline"),
        max_length=255,
        blank=True,
        null=True
    )
    text = models.TextField(
        _(u"Timeline Headline"),
        blank=True,
        null=True
    )
    start_date = models.DateField(
        _(u'Timeline start date'),
        blank=True,
        null=True
    )
    end_date = models.DateField(
        _(u'Timeline start date'),
        blank=True,
        null=True
    )
    tag = models.CharField(
        _(u"Tag"),
        max_length=140,
        null=True,
        blank=True
    )
    value = models.CharField(
        _(u"Chart Value"),
        max_length=140,
        null=True,
        blank=True,
        help_text=_(u'This is only used for "chart" type')
    )
    classname = models.CharField(
        _(u"Classname"),
        max_length=255,
        null=True,
        blank=True
    )
    media = models.TextField(
        _(u"Media"),
        blank=True,
        null=True,
    )
    caption = models.CharField(
        _(u"Media caption"),
        max_length=255,
        blank=True,
        null=True,
    )
    credit = models.CharField(
        _(u"Media credit"),
        max_length=255,
        blank=True,
        null=True,
    )
    thumbnail = models.CharField(
        _(u"Media thumbnail"),
        max_length=500,
        blank=True,
        null=True,
        help_text=_(u'Optional 32x32 thumbnail')
    )
    order = models.IntegerField(_(u"Order"), default=0)

    __unicode__ = lambda self: self.headline


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
            raise ValidationError(_(u'Infographic date_available '
                                    u'is greater than today!'))


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
        unique_together = (
            "key_group", "key", "site",
            "channel", "article", "infographic"
        )
