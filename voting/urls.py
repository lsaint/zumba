
from django.conf.urls import include, url
from django.views.decorators.cache import cache_page

import voting.views as views

urlpatterns = [
    url(r'^i/$', views.index, name='index'),
    url(r'^(?P<topic_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<topic_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^leaderboard/(?P<kind>\w+)/$', cache_page(5)(views.leaderboard), name='leaderboard'),
    url(r'^zumbalogin/$', views.zumbalogin, name='zumbalogin'),
    url(r'^uploaded/$', views.uploaded, name='uploaded'),

    url(r'^pullboard/(?P<kind>\w+)/(?P<offset>[0-9]+)/(?P<limit>[0-9]+)/$',
                                         cache_page(5)(views.pullboard), name='pullboard'),
]
