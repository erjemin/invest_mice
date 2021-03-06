# -*- coding: utf-8 -*-
# Включили поддержку UTF-8 в Python. Без этого даже комментарии на русском языке нельзя писать.
# from django.conf.urls import *
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from www.views import hello
from www.parser import parsRBC
from www.indicator import indicator

urlpatterns = patterns('',
    ( r'^hello/$', hello ),
    ( r'^parser/(\S{0,16})/(\S{0,3})/$', parsRBC ), # передаем два параметра (если получится)
#    ( r"^indicator/(\S{0,16})/(\d{0,4}[-]?\d{0,2}[-]?\d{0,2})/(\S{0,4})/$", indicator),
    ( r"^indicator/(\S{0,16})/(\d{0,4}[-]?\d{0,2}[-]?\d{0,2})/(\S{0,4})/$", indicator),
    # Examples:
    # url(r'^$', 'invest_mice.views.home', name='home'),
    # url(r'^invest_mice/', include('invest_mice.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)






