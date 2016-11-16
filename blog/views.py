from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import json
from django.forms.models import modelform_factory
from django.views.generic import View
from user.models import User, Author, Image
from audio.models import Audio
from .models import Post, Comment
import sys
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User as djUser

class Wall(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, path):
        try:
            posts = User.objects.get(id=int(path)).wall.all()
            user = User.objects.get(id=int(path))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error masage' : 'does not exist'}), content_type="application/json")
        except:
            posts = []
            print ()
        return render(request, "wall.html", {'posts': posts, 'user': user})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request, path):
        if ('post_text' in request.POST):
            try:
                Post.objects.create(text = request.POST['post_text'], creator = request.user.customUser, owner = User.objects.get(id=int(path)))
            except User.DoesNotExist:
                return self.get(request, path)
            except:
                print("Unexpected error:", sys.exc_info())
        if ('audio' in request.POST):
            f = 4 #TODO

        try:
            posts = User.objects.get(id=int(path)).wall.all()
            user = User.objects.get(id=int(path))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error masage' : 'does not exist'}), content_type="application/json")
        except:
            posts = []
            print ()
        return render(request, "wall.html", {'posts': posts, 'user': user})