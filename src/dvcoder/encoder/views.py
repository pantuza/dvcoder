# -*- coding: utf8 -*-

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.generic import View
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.conf import settings
from boto import connect_s3
from boto.s3.key import Key
from os import remove
from os.path import join


class EncoderView(View):


    def get(self, request):
        return render_to_response('encoder.html',
               context_instance=RequestContext(request))

    def post(self, request):

        file = request.FILES['dvfile']
        tmp_path = join(settings.MEDIA_ROOT,'tmp/%s' % file.name)
        filepath = default_storage.save(tmp_path, ContentFile(file.read()))

        try:
            self.push_to_s3(filepath)
        except Exception as s3Exception:
            raise s3Exception

        return redirect('/')

    def push_to_s3(self, filepath):

        filename = filepath.split("/")[-1]
        boto = connect_s3()
        bucket = boto.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        mykey = Key(bucket)
        mykey.key = "videos/%s" % filename
        mykey.set_contents_from_filename(filepath)
        mykey.make_public()
        remove(filepath)
