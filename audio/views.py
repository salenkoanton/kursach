from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User as djUser
from user.models import User, Author, Image
class Playlist(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        user = request.user
        playlist = user.customUser.audio.all()
        return render(request, "playlist.html", {'playlist' : playlist})

# Create your views here.
