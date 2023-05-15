from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Comment, Post, CustomUser, Tag
from django.utils.text import slugify

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'What is your thought?'})
        }

class NewPostForm(forms.ModelForm):
   
    class Meta:
        model = Post
        fields = ('title', 'body', 'image', 'status', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Title'}),
            'body': forms.Textarea(attrs={'placeholder':'Write Your Article Here'}),
           
        }
    def __init__(self, *args,**kwargs):
        if kwargs.get('request'):
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


    def save(self, commit=True):
        tag = self.cleaned_data.pop('tags')
        post = Post.objects.create(**self.cleaned_data)
        post.tags.add(*tag)
        post.author = self.request.user
        post.slug = slugify(post.title)
        post.save()
        return  post
    
   

        
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'avatar' ]
        widgets = {
        'username': forms.TextInput(attrs={'class':'form-control', }),
        'email': forms.TextInput(attrs={'class':'form-control', }),
    }
    
class DraftForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'image', 'status', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Title'}),
            'body': forms.Textarea(attrs={'placeholder':'Write Your Article Here'}),
           
        }
    def __init__(self, *args,**kwargs):
        if kwargs.get('request'):
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


    def save(self, commit=True):
        tag = self.cleaned_data.pop('tags')
        post = Post.objects.create(**self.cleaned_data)
        post.tags.add(*tag)
        post.author = self.request.user
        post.slug = slugify(post.title)
        post.save()
        return  post
    