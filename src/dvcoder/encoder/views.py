# -*- coding: utf8 -*-

from django.views.generic import View
from django.shortcuts import render_to_response

class EncoderView(View):


    def get(self, request):
        return render_to_response('encoder.html')

    def post(self, request):
        pass
