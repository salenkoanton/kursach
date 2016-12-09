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
from .forms import PostImageForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User as djUser
from audio.views import handle_uploaded_file
from audio.forms import UploadFileForm
from django.shortcuts import redirect
class Wall(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, path):
        try:
            xhr = request.GET['xhr']
        except:
            xhr = False
        if xhr == 'true':
            print (request.META["QUERY_STRING"])
            return redirect('/search' + '?' + request.META["QUERY_STRING"])
        print(request.GET)
        try:

            posts = User.objects.get(id=int(path)).wall.all()
            user = User.objects.get(id=int(path))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error masage' : 'does not exist'}), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'error masage' : 'server error'}), content_type="application/json")

        return render(request, "wall.html", {'posts': posts, 'user': user, 'you': request.user.customUser})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request, path):
        print(request.POST)
        print(request.FILES)
        if 'comment_text' in request.POST:
            try:
                Comment.objects.create(text = request.POST['comment_text'], post = Post.objects.get(id=request.POST['id']), owner = request.user.customUser)
            except:
                print("Unexpected error:", sys.exc_info())
        elif 'post_text' in request.POST:
            try:
                audios_id = []
                try:
                    if request.POST['audios'] != '':
                        if request.POST['audios'].find('_') != -1:
                            audios_id = request.POST['audios'].split('_')
                        else:
                            audios_id.append(request.POST['audios'])
                        print(request.POST['audios'])

                except:
                    print('error in audio')
                images = []
                try:
                    if 'post_image' in request.FILES:
                        form = PostImageForm(request.POST, request.FILES)
                        if form.is_valid():
                            #handle_uploaded_file(request.FILES['post_image'])
                            img = Image.objects.create(file=request.FILES['post_image'])
                            img.save()
                            images.append(img)
                        else:
                            print('form invalid')
                except:
                    print("Unexpected error:", sys.exc_info())
                p = Post.objects.create(text = request.POST['post_text'], creator = request.user.customUser, owner = User.objects.get(id=int(path)))
                for audio in audios_id:
                    p.audio.add(Audio.objects.get(id=int(audio)))
                for img in images:
                    p.image.add(img)
                p.save()
            except:
                print("Unexpected error:", sys.exc_info())
        elif 'like' in request.POST:
            user = request.user
            params = request.POST
            try:
                xhr = request.POST['xhr']
            except:
                xhr = False
            response_dict = {}
            print(request.POST)
            try:
                p = Post.objects.get(id=request.POST['like'])
                if p.likes.filter(id = request.user.customUser.id).exists():
                    p.likes.through.objects.get(post_id = p.id, user_id = request.user.customUser.id).delete()
                else:
                    p.likes.add(request.user.customUser)
                p.save()
                response_dict = {'status': 'ok', 'likes_count' : p.likes.count()}
            except:
                print("Unexpected error:", sys.exc_info())
                response_dict = {'status': 'error'}
            if xhr == 'true':
                return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
        elif 'follow' in request.POST:
            try:
                u = User.objects.get(id=request.POST['follow'])
                if u.followers.filter(id = request.user.customUser.id).exists():
                    u.followers.through.objects.get(from_user = u, to_user = request.user.customUser).delete()
                else:
                    u.followers.add(request.user.customUser)
                u.save()
            except:
                print("Unexpected error:", sys.exc_info())
        elif 'image' in request.FILES:
            try:
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    handle_uploaded_file(request.FILES['image'])
                else:
                    HttpResponse(json.dumps({'error': 'form invalid'}), content_type="application/json")
                i = Image.objects.create(file = request.FILES['image'])
                request.user.customUser.avatar = i
                i.save()
                request.user.customUser.save()
                print(i)

            except:
                print("Unexpected error:", sys.exc_info())
        elif 'add' in request.POST:
            user = request.user
            params = request.POST
            try:
                xhr = request.POST['xhr']
            except:
                xhr = False
            response_dict = {}
            print(request.POST)
            try:
                user.customUser.audio.add(Audio.objects.get(id=int(params['add'])))
                response_dict = {'status': 'ok'}
            except:
                print("Unexpected error:", sys.exc_info())
                response_dict = {'status': 'error'}
            if xhr == 'true':
                return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
            return self.get(request, path)
        try:
            posts = User.objects.get(id=int(path)).wall.all()
            user = User.objects.get(id=int(path))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error masage' : 'does not exist'}), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'error masage': 'server error'}), content_type="application/json")
        return render(request, "wall.html", {'posts': posts, 'user': user, 'you': request.user.customUser})
@login_required(login_url='/login/')
def followers(request, path):
    user = User.objects.get(id=int(path))
    f = user.followers.all()
    return render(request, "followers.html", {'you': request.user.customUser, 'followers': f, 'follow': True})
@login_required(login_url='/login/')
def following(request):
    f = request.user.customUser.following.all()
    return render(request, "followers.html",
                  {'you': request.user.customUser, 'followers': f, 'follow': False})