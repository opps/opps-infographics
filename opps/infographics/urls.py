#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls import patterns, url

from .views import InfographicDetail, InfographicList, ChannelInfographicList


urlpatterns = patterns(
    '',
    url(r'^$', InfographicList.as_view(), name='list_infographic'),
    url(r'^channel/(?P<channel__long_slug>[\w//-]+)$', ChannelInfographicList.as_view(),
        name='channel_infographic'),
    url(r'^(?P<slug>[\w-]+)/(?P<result>[\w-]+)$',
        InfographicDetail.as_view(), name='result_infographic'),
    url(r'^(?P<slug>[\w-]+)$',
        InfographicDetail.as_view(), name='open_infographic'),

)
