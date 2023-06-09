from django import template
from django.db.models import Count
from ..models import Post

register = template.Library()

@register.simple_tag

def total_posts():
    return Post.objects.count()



@register.inclusion_tag('post/latest_posts.html')
def display_latest_posts(count=5):
    latest_posts = Post.objects.filter(status='published').order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_comments=Count('comment')).order_by('-total_comments')[:count]