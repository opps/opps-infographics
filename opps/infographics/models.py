# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from opps.core.models import Publishable
from opps.core.models import Slugged
from opps.core.tags.models import Tagged

app_namespace = getattr(settings, 'OPPS_INFOGRAPHICS_URL_NAMESPACE', 'infographics')

CSS_TEXT = getattr(
    settings,
    'OPPS_INFOGRAPHICS_CSS_TEXT',
    """
    .infographic-box {

    }
    #infographic-top-image {

    }
    #infographic-top-image img {

    }
    #infographic-menu-items {
        position:relative; top:-42px;
    }
    #infographic-menu-items .menu {
        list-style:none;
    }
    #infographic-menu-items .item-menu {
        float:left;
        margin-right:10px;
    }
    #infographic-menu-items .item-menu a {
        color: #FFA500;
    }
    #infographic-menu-items .item-menu a.item-active {
       color:#FFFFFF;
    }

    #infographic-content {
       clear:both;
       width:960px;
    }
    #infographic-item-description {
       float:left;
       max-width:320px;
       height:400px;
       width:320px;
       overflow-y:scroll
    }
    #infographic-item-image {
       float:right;
       width:600px;
    }
    """
)


class Infographic(Publishable, Slugged, Tagged):

    TYPES = (
        ("gallery", _(u"Photo Gallery")),
        ("timeline", _(u"Timeline")),
    )
    title = models.CharField(_(u"Title"), max_length=255)
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
    containers = models.ManyToManyField(
        'containers.Container',
        null=True,
        blank=True,
        related_name='infographic_container',
        through='InfographicContainer'
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
    css_text = models.TextField(
        _(u"CSS"),
        blank=True,
        null=True,
        default=CSS_TEXT,
        help_text=_(u'Custom in-page css applied in all infographics type')
    )

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
        'timelinejs.Timeline',
        verbose_name=_(u'Timeline'),
        null=True,
        blank=True,
        related_name='infographic_timeline',
        on_delete=models.SET_NULL,
        help_text=_(u'Set this and provide JSON, DOC or Events')
    )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['order']
        unique_together = ['site', 'slug']
        verbose_name = _(u'Infographic')
        verbose_name_plural = _(u'Infographics')

    def get_absolute_url(self):
        return reverse(
            '{0}:open_infographic'.format(app_namespace),
            kwargs={'slug': self.slug}
        )

    def get_thumb(self):
        return self.main_image

    @property
    def search_category(self):
        return _("Infographic")


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


class InfographicContainer(models.Model):
    container = models.ForeignKey(
        'containers.Container',
        verbose_name=_(u'Infographic Container'),
        null=True,
        blank=True,
        related_name='infographiccontainer_container',
        on_delete=models.SET_NULL
    )
    infographic = models.ForeignKey(
        'infographics.Infographic',
        verbose_name=_(u'Infographic'),
        null=True,
        blank=True,
        related_name='infographiccontainer_infographic',
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return u"{0}-{1}".format(self.infographic.slug, self.container.slug)

    class Meta:
        verbose_name = _(u'Infographic Container')
        verbose_name_plural = _(u'Infographic Containers')


class InfographicItem(models.Model):
    title = models.CharField(_(u"Title"), max_length=255)
    slug = models.SlugField(
        _(u"URL"),
        max_length=150,
        db_index=True
    )
    description = models.TextField(_(u"Description"), null=True, blank=True)

    # optional for gallery and css
    group = models.CharField(
        _(u"Group"),
        max_length=255,
        blank=True, null=True,
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

    timeline = models.ForeignKey(
        'timelinejs.Timeline',
        verbose_name=_(u'Timeline'),
        null=True,
        blank=True,
        related_name='infographicitem_timeline',
        on_delete=models.SET_NULL,
        help_text=_(u'Set this and provide JSON, DOC or Items')
    )

    order = models.IntegerField(_(u"Order"), default=0)

    css_text = models.TextField(
        _(u"CSS"),
        blank=True,
        null=True
    )

    def belongs(self):
        if not self.infographicitem_item.exists():
            return _(u"No infographic")

        return ", ".join(item.infographic.title for item in self.infographicitem_item.all())

    __unicode__ = lambda self: self.title

    class Meta:
        verbose_name = _(u'Infographic Item')
        verbose_name_plural = _(u'Infographic Items')
