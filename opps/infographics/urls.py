#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls import patterns, url

from .views import InfographicDetail, InfographicList, ChannelInfographicList


urlpatterns = patterns(
    '',
    url(
        r'^$',
        InfographicList.as_view(),
        name='list_infographic',
    ),
    url(
        r'^channel/(?P<channel__long_slug>[\w//-]+)$',
        ChannelInfographicList.as_view(),
        name='channel_infographic',
    ),
    url(
        r'^(?P<slug>[\w-]+)/(?P<item_slug>[\w-]+)$',
        InfographicDetail.as_view(),
        name='item_infographic',
    ),
    url(
        r'^(?P<slug>[\w-]+)$',
        InfographicDetail.as_view(),
        name='open_infographic',
    ),
)
