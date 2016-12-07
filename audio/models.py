from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.models import User, Author
# Create your models here.
class Audio(models.Model):
    ROCK = 'rock'
    METAL_CORE = 'met_c'
    METAL = 'metal'
    HARD_CORE = 'hd_c'
    RAP = 'rap'
    TYPE = (
        (ROCK, 'rock'),
        (METAL_CORE, 'metalcore'),
        (METAL, 'metal'),
        (HARD_CORE, 'hardcore'),
        (RAP, 'rap'),
    )
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    author = models.ForeignKey('user.Author', on_delete=models.CASCADE, related_name='audio')
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to = 'audio/', default=None)
    type = ArrayField(models.CharField(max_length=5, choices=TYPE), size = 40)
    duration = models.TimeField(default=None)
    def dict(self):
        return  {'id' : self.id,
                 'author': {'id' : self.author.id,
                            'name' : self.author.name},
                 'name': self.name,
                 'url': self.file.url,
                 'types': [i for i in self.type]}
