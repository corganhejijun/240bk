from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Data/html/(?P<aid>[0-9]+)/$', views.aidPage),
    url(r'^Ftp$', views.ftp, name='ftp'),
]
