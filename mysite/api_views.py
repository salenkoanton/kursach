from django.shortcuts import render
from django.contrib.auth.models import User as djUser
from mysite import settings
from audio.forms import UploadFileForm
import os
from audio.models import Audio
import json
from django.forms.models import modelform_factory
from django.views.generic import View
from user.models import User, Image, Author
from blog.models import Post, Comment
import sys
from django.http import HttpResponse
from django.contrib.auth.models import User as DJangoUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as djlogout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

#return HttpResponse(json.dumps(response_data), content_type="application/json")
def handle_uploaded_file(f):
    with open(os.path.join(settings.MEDIA_ROOT, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
class Playlist(View):
    @method_decorator(login_required(login_url='/api/login/'))
    def get(self, request):
        user = request.user
        playlist = user.customUser.audio.all()
        response_data = [i.dict() for i in playlist]
        return HttpResponse(json.dumps(response_data), content_type="application/json" )
    @method_decorator(login_required(login_url='/api/login/'))
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
        try:
            user = User.objects.get(id=int(path))
        except:
            return HttpResponse(json.dumps({'error': 'doesNotExist'}), content_type="application/json")
        print(request)
        response_data = [i.dict() for i in user.audio.all()]
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class Users_id(View):
    @method_decorator(login_required(login_url='/api/login/'))
    def get(self, request, path):
        try:
            response_data = User.objects.get(id=int(path)).dict()
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error massage': 'wrong id'}), content_type="application/json")
        except:
            print("Unexpected error:", sys.exc_info())
            return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    @method_decorator(login_required(login_url='/api/login/'))
    def post(self, request, path):
        params_to_parse = request.META['QUERY_STRING']
        print(request.get_full_path())
        params = dict([p.split('=') for p in params_to_parse.split('&')])
        try:
            print(params['follow'])
            User.objects.get(id=int(path)).follow(params['follow'])
        except:
            print('not follow')
        return self.get(request, path)


class Users_id_wall(View):
    @method_decorator(login_required(login_url='/api/login/'))
    def get(self, request, path):
        try:
            response_data = [i.dict() for i in User.objects.get(id=int(path)).posts.all()]
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error massage': 'wrong id'}), content_type="application/json")
        except:
            print("Unexpected error:", sys.exc_info())
            return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    @method_decorator(login_required(login_url='/api/login/'))
    def post(self, request, path):
        params_to_parse = request.META['QUERY_STRING']
        params = dict([p.split('=') for p in params_to_parse.split('&')])
        try:
            print(params)
            Post.objects.create(text=params['text'], creator=User.objects.get(id=int(params['creator'])),
                                owner=User.objects.get(id=int(path)))
        except:
            print('not post post')
            print("Unexpected error:", sys.exc_info())
        return self.get(request, path)


class Users_id_followers(View):
    @method_decorator(login_required(login_url='/api/login/'))
    def get(self, request, path):
        try:
            response_data = [i.dict() for i in User.objects.get(id=int(path)).followers.all()]
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error massage': 'wrong id'}), content_type="application/json")
        except:
            print("Unexpected error:", sys.exc_info())
            return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/api/login/')
def users(request):
    try:
        response_data = [i.dict() for i in User.objects.all()]
    except:
        print("Unexpected error:", sys.exc_info())
        return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
    print(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


class Logout(View):
    def get(self, request):
        djlogout(request)
        return redirect('/api/login/')


class Login(View):
    def get(self, request):
        isLogin = request.user.is_authenticated()
        return HttpResponse(json.dumps({'login': isLogin}), content_type="application/json")

    def post(self, request):
        params = request.POST
        print(params['email'])
        if params['email'].find('@') == -1:
            username = params['email']
        else:
            try:
                username = User.objects.get(djangoUser__email=params['email']).djangoUser.username
            except:
                print('error')
                username = None
                return render(request, 'login.html', {})
        user = authenticate(username=username, password=params['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    print(request.GET['next'])
                    return redirect(request.GET['next'])
                except:
                    return redirect('/api/blog/' + str(user.customUser.id) + '/wall')
            else:
                return HttpResponse(json.dumps({'login': 'error disabled'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'login': "error pass don't manch"}), content_type="application/json")


def auth(request):
    if request.method == 'POST':
        params = request.POST
        print(params.keys())
        try:
            try:
                user = DJangoUser.objects.get(username=params['username'])
                if user is not None:
                    return HttpResponse(json.dumps({'error': 'Error, we already have a user with such name'}), content_type="application/json" )
            except:
                print(params)
                try:
                    print(params['email'])
                    user = DJangoUser.objects.get(email=params['email'])
                    print(user)
                    if user is not None:
                        return HttpResponse(json.dumps({'error': 'Error, we already have a user with such email'}),
                                            content_type="application/json")
                except:
                    print(sys.exc_info())
                    print('success')
            user = DJangoUser.objects.create_user(params['username'], params['email'], params['password'])
            user.last_name = params['lastname']
            user.first_name = params['firstname'];
            user.save()
            cus_us = User.objects.create(djangoUser=user, birthdate=params['birthdate'])
            if params['sex'] == 'male':
                cus_us.sex = True
                cus_us.avatar = User.MALE_AVATAR
            else:
                cus_us.sex = False
                cus_us.avatar = User.FEMALE_AVATAR
            cus_us.save()
        except ValueError:
            params = {}
        print(params)
        return HttpResponse(json.dumps({'signup': 'ok'}),
                            content_type="application/json")


def main(request):
    return HttpResponse(json.dumps({'smth text': 'ok'}),
                            content_type="application/json")


def author(request, path):
    a = Author.objects.get(id=int(path))
    return HttpResponse(json.dumps(a.dict()),
                 content_type="application/json")

def authors(request):
    if request.user.is_authenticated():
        you = request.user
    else:
        you = None
    a = Author.objects.all()
    response_data = [i.dict() for i in a]
    return HttpResponse(json.dumps(response_data), content_type="application/json")

class Wall(View):
    @method_decorator(login_required(login_url='/api/login/'))
    def get(self, request, path):
        try:
            posts = User.objects.get(id=int(path)).wall.all()
            user = User.objects.get(id=int(path))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error masage' : 'does not exist'}), content_type="application/json")
        except:
            posts = []
            print ()
            return HttpResponse(json.dumps({'error masage': 'server error'}), content_type="application/json")
        response_data = [i.dict() for i in posts]
        return HttpResponse(json.dumps(response_data), content_type="application/json")


    @method_decorator(login_required(login_url='/api/login/'))
    def post(self, request, path):
        print(request.POST)
        if 'comment_text' in request.POST:
            try:
                Comment.objects.create(text = request.POST['comment_text'],
                                       post = Post.objects.get(id=request.POST['id']),
                                       owner = request.user.customUser)
                return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")
            except:
                print("Unexpected error:", sys.exc_info())
                return HttpResponse(json.dumps({'status': 'bad'}), content_type="application/json")
        elif ('post_text' in request.POST):
            try:
                Post.objects.create(text = request.POST['post_text'], creator = request.user.customUser, owner = User.objects.get(id=int(path)))
                return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")
            except:
                print("Unexpected error:", sys.exc_info())
                return HttpResponse(json.dumps({'status': 'bad'}), content_type="application/json")
        elif 'like' in request.POST:
            try:
                p = Post.objects.get(id=request.POST['like'])
                if p.likes.filter(id = request.user.customUser.id).exists():
                    p.likes.through.objects.get(post_id = p.id, user_id = request.user.customUser.id).delete()
                else:
                    p.likes.add(request.user.customUser)
                p.save()
                return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")
            except:
                print("Unexpected error:", sys.exc_info())
                return HttpResponse(json.dumps({'status': 'bad'}), content_type="application/json")
        elif 'follow' in request.POST:
            try:
                u = User.objects.get(id=request.POST['follow'])
                if u.followers.filter(id = request.user.customUser.id).exists():
                    u.followers.through.objects.get(from_user = u, to_user = request.user.customUser).delete()
                else:
                    u.followers.add(request.user.customUser)
                u.save()
                return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")
            except:
                print("Unexpected error:", sys.exc_info())
                return HttpResponse(json.dumps({'status': 'bad'}), content_type="application/json")
        return HttpResponse(json.dumps({'status': 'wrong args'}), content_type="application/json")
@login_required(login_url='/api/login/')
def following(request):
    f = request.user.customUser.following.all()
    respons_data = [i.dict() for i in f]
    return HttpResponse(json.dumps(respons_data), content_type="application/json")