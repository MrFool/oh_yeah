from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<fund_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<fund_id>[0-9]+)/approve', views.approve, name='approve'),
    url(r'^(?P<fund_id>[0-9]+)/deny', views.deny, name='deny'),
]
