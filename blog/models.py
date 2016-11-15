from django.db import models
from django.utils import timezone
from audio.models import Audio
from user.models import User, Author, Image

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=True)
    creator = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='created_posts', null=True)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='wall', null=True)
    audio = models.ManyToManyField('audio.Audio', related_name='post')
    image = models.ManyToManyField('user.Image', related_name='post')
    likes = models.ManyToManyField('user.User', related_name='liked')
    def like(self, User_id):
        self.likes.add(User.objects.get(id=User_id))
    def dict(self):
        return  {'id' : self.id,
                 'text': self.text,
                 'creator': self.creator.id,
                 'comments': [i.id for i in self.comments.all()],
                 'audio' : [i.id for i in self.audio.all()],
                 'images': [{'id': i.id,
                             'url':i.url} for i in self.image.all()]}
    class Meta:
        ordering = ('id',)
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='comments')
    def dict(self):
        return {'id' : self.id,
                'text': self.text,
                'post': {'id': self.post.id},
                'owner': {'id':self.owner.id,
                          'name':self.owner.name}}