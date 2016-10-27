from django.conf.urls import patterns, include, url
from django.contrib import admin

from worth_schedule import views as v

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cambast.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', v.ranking_page),
    url(r'^add-raw-currency$', v.add_currency_raw),
    url(r'^add-raw-event$', v.add_event_raw),
    url(r'^finish/(.*)$', v.finish),
    url(r'^admin/', include(admin.site.urls)),
)
