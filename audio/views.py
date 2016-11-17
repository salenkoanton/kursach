from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User as djUser
from user.models import User, Author, Image
from mysite import settings
from .forms import UploadFileForm
import os, sys
from .models import Audio
def handle_uploaded_file(f):
    with open(os.path.join(settings.MEDIA_ROOT, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
class Playlist(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        user = request.user
        playlist = user.customUser.audio.all()
        return render(request, "playlist.html", {'playlist' : playlist, 'you': request.user.customUser, 'user' : None})
    def post(self, request):
        user = request.user
        params = request.POST

        try:
            author = Author.objects.get(name = params['author'])
        except:
            author = Author.objects.create(name = params['author'], information = '')
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['audio'])
        a = Audio.objects.create(text = params['post_text'],
                                 author = author,
                                 name = params['name'],
                                 file = request.FILES['audio'],
                                 type = [params['type']],
                                 duration = '00:00:00')
        user.customUser.audio.add(a)
        a.save()
        return self.get(request)
class Audios_id(View):
    def post(self, request, path):
        user = request.user
        params = request.POST
        try:
            user.customUser.audio.add(Audio.objects.get(id=int(params['add'])))
        except:
            print("Unexpected error:", sys.exc_info())
        return self.get(request, path)
    def get(self, request, path):

        user = User.objects.get(id=int(path))
        print(request)
        return render(request, "playlist.html", {'playlist' : user.audio.all(),
                                                 'user' : user,
                                                 'you': request.user.customUser})
    # Create your views here.
