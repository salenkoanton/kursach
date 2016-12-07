from django import forms

class PostImageForm(forms.Form):
    post_image = forms.ImageField()
