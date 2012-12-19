from django.conf.urls import patterns, include, url
from encoder.views import EncoderView
from video.views import VideoView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', EncoderView.as_view(), name='encoder'),

    url(r'^video/(?P<video>.*)$', VideoView.as_view(), name='video'),
    # url(r'^dvcoder/', include('dvcoder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
