from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as DJangoUser
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(null=True)
    file = models.ImageField(upload_to = 'img/', null=True)
    def dict(self):
        return {'id': self.id, 'url': self.file.url}
class User(models.Model):
    SEX = (
        (True, 'male'),
        (False, 'female')
    )
    id = models.AutoField(primary_key=True)
    try:
        MALE_AVATAR = Image.objects.get(id=5)
        FEMALE_AVATAR = Image.objects.get(id=6)
    except:
        MALE_AVATAR = None
        FEMALE_AVATAR = None
    djangoUser = models.OneToOneField(DJangoUser, on_delete=models.CASCADE, related_name='customUser', null=True)
    sex = models.NullBooleanField(default=True, blank=True, null=True, choices=SEX)
    created_date = models.DateTimeField(default=timezone.now, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    avatar = models.ForeignKey('Image', on_delete=models.CASCADE, blank=True, null=True)
    birthdate = models.DateField(default=None, null=True)
    audio = models.ManyToManyField('audio.Audio', related_name='users')
    def follow(self, user_id):
        self.following.add(User.objects.get(id=user_id))
    def dict(self):
        return {'id': self.id,
                'username': self.djangoUser.username,
                'first_name': self.djangoUser.first_name,
                'last_name': self.djangoUser.last_name,
                'sex': self.get_sex_display(),
                'avatar': self.avatar.id,
                'followers': [{'id': i.id} for i in self.followers.all()],
                'audio': [{'id': i.id,
                           'author_id': i.author.id,
                           'name': i.name} for i in self.audio.all()],
                'wall': [{'id': i.id} for i in self.wall.all()]}
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    information = models.TextField(default=None, null=True)
    def dict(self):
        return {'id' : self.id,
                'name': self.name,
                'information': self.information,
                'songs' : [{'id':i.id,
                            'name':i.name} for i in self.audio.all()]}

# Create your models here.

