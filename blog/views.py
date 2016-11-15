from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import json
from django.forms.models import modelform_factory
from django.views.generic import View
from user.models import User, Author, Image
from .models import Post, Comment
import sys
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
@login_required(login_url='/login/')
def wall(request, path):
    try:
        posts = User.objects.get(id=int(path)).wall.all()
        user = User.objects.get(id=int(path))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'error masage' : 'does not exist'}), content_type="application/json")
    except:
        posts = []
        print ()
    return render(request, "wall.html", {'posts': posts, 'user': user})