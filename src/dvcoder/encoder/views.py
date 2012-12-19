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
from zencoder import Zencoder
import time


class EncoderView(View):

    # nome arquivo de entrada 
    filename = None
    # atributo da classe que guarda o nome do vídeo encodado
    video_name = None
    # bucket connection
    bucket = None

    def get(self, request):

	return render_to_response('encoder.html',
               context_instance=RequestContext(request))

    def post(self, request):

        file = request.FILES['dvfile']
        tmp_path = join(settings.MEDIA_ROOT,'tmp/%s' % file.name)
        filepath = default_storage.save(tmp_path, ContentFile(file.read()))

        try:
            self.push_to_s3(filepath)

	    if not self.filename or not self.bucket:
	        raise Exception('Falha ao fazer upload de arquivo')

	    self.encode()

        except Exception as s3Exception:
            raise s3Exception

	return redirect('/video/%s/' % self.video_name)


    def push_to_s3(self, filepath):

        self.filename = filepath.split("/")[-1]
        boto = connect_s3()
        self.bucket = boto.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        mykey = Key(self.bucket)
        mykey.key = "videos/%s" % self.filename
        mykey.set_contents_from_filename(filepath)
        mykey.make_public()
        remove(filepath)


    def encode(self):

	zen = Zencoder('75ffab0006cbaac5e293fa40e80647d0')
	input_url = 's3://dvcoder/videos/%s' % self.filename

	try:
	    cut_point = self.filename.rindex('.')
	    output_filename = self.filename[0:cut_point]
	except ValueError:
	    output_filename = self.filename

	video = {'label': 'sambatech',
  	         'url': 's3://dvcoder/encoded/%s.mp4' % output_filename,
	         'width': 480,
	         'height': 320}
	outputs = (video)
	self.video_name = "%s.mp4" % output_filename

	job = zen.job.create(input_url, outputs=outputs)
	job_id = job.body['id']

	progress = zen.job.details(job_id)
	state = progress.body['job']['state']
	while state in ('pending', 'waiting', 'processing'):
	    time.sleep(5)
	    progress = zen.job.details(job_id)
	    state = progress.body['job']['state']
	    print state
	
	if state != 'finished':
	    print "Nurse, we have a problem: ", progress
	    self.video_name = None

	else:
            newkey = Key(self.bucket)
	    newkey.key = "encoded/%s" % self.video_name
	    newkey.make_public()
