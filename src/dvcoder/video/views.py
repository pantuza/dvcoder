# -*- coding: utf-8 -*-

from django.views.generic import View
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.conf import settings

class VideoView(View):

    def get(self, request, video=None):

	print video
	if video is None:
	    return redirect('/')
	url = "%sencoded/%s" % (settings.S3_URL, video)
	template_vars = {'video': url}
        return render_to_response('video.html', template_vars)
