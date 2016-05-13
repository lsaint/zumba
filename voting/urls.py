
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

import voting.views as views

urlpatterns = [
    url(r'^i/$', views.main, name='main'),
    url(r'^up/$', views.up, name='up'),
    url(r'^(?P<topic_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<topic_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^zumbalogin/$', views.zumbalogin, name='zumbalogin'),
    url(r'^uploaded/$', views.uploaded, name='uploaded'),
    url(r'^pullboard/(?P<kind>\w+)/(?P<offset>[0-9]+)/(?P<limit>[0-9]+)/$',
                                         cache_page(5)(views.pullboard), name='pullboard'),

    url(r'^index/', TemplateView.as_view(template_name="voting/index.html"), name='index'),
    url(r'^list/', TemplateView.as_view(template_name="voting/list.html"), name='list'),
    url(r'^active_choose/', TemplateView.as_view(template_name="voting/active_choose.html"), name='active_choose'),
    url(r'^active_choose2/', TemplateView.as_view(template_name="voting/active_choose2.html"), name='active_choose2'),
    url(r'^guide/', TemplateView.as_view(template_name="voting/guide.html"), name='guide'),
    url(r'^guide_inner/', TemplateView.as_view(template_name="voting/guide_inner.html"), name='guide_inner'),
    url(r'^photo_alls/', TemplateView.as_view(template_name="voting/photo_alls.html"), name='photo_alls'),
    url(r'^photo_up/', TemplateView.as_view(template_name="voting/photo_up.html"), name='photo_up'),
    url(r'^video_go/', TemplateView.as_view(template_name="voting/video_go.html"), name='video_go'),
    url(r'^photo_alls_inner/', TemplateView.as_view(template_name="voting/photo_alls_inner.html"), name='photo_alls_inner'),
    url(r'^new_pic/', TemplateView.as_view(template_name="voting/new_pic.html"), name='new_pic'),
]
