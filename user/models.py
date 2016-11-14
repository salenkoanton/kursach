from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    followers = models.ManyToManyField('User', related_name='following')
    #avatar = models.ForeignKey('Image', on_delete=models.CASCADE, default=None)
    birthdate = models.DateField(default=None)
    audio = models.ManyToManyField('audio.Audio', related_name='users')
    def follow(self, user_id):
        self.following.add(User.objects.get(id=user_id))
    def dict(self):
        return {'id':self.id,
                'name':self.name,
                'followers':[{'id': i.id} for i in self.followers.all()],
                'audio': [{'id': i.id,
                           'author': i.author,
                           'name': i.name} for i in self.audio.all()],
                'wall': [{'id': i.id for i in self.posts.all()}]}
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    information = models.TextField(default=None)
    def dict(self):
        return {'id' : self.id,
                'name': self.name,
                'information': self.information,
                'songs' : [{'id':i.id,
                            'name':i.name} for i in self.audio.all()]}
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    file = models.FileField(default=None)
    def dict(self):
        return {'id': self.id, 'url': self.url}
# Create your models here.

