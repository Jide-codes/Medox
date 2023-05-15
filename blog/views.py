from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag, Comment, CustomUser
from .forms import EmailPostForm, CommentForm, NewPostForm, UserForm, DraftForm
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
import math
# Create your views here.



# class PostListView(ListView):

#     queryset = Post.objects.all()
#     context_object_name = "posts"
#     paginate_by = 3
#     template_name = 'post/list.html'



@login_required
def new_post(request):
   
    post_form =NewPostForm()
    if request.method == 'POST':
        post_form = NewPostForm(request.POST, request.FILES, request=request)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, "Post has been published !! ")
            return redirect('/')
        else:
            messages.error(request, "Oops! An error ocurr ")
            post_form = NewPostForm(request=request)
    context = {
            'form':post_form
            }
    return render(request, 'post/newpost.html', context)

@login_required
def post_list(request):
    
    tags = Tag.objects.all()
    object_list = Post.objects.filter(status='published')
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')

    try:

        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts':posts,
        'page':page,    
        'tags': tags
    }
    return render(request, 'post/list.html', context)


def calculate_reading_time(content):
    words = strip_tags(content).split()
    word_count = len(words)

    avg_reading_speed = 200
    read_time_minutes = math.ceil(word_count / avg_reading_speed)
    return read_time_minutes


@login_required
def post_details(request, year, month, day, slug ):
    post = get_object_or_404(Post, slug=slug, publish__year=year, 
                             publish__month=month,
                             publish__day=day)

    
    # list of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids,  status='published').exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]


    read_time_minutes = calculate_reading_time(post.body)
 

    # Comment section

    comments = post.comment.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
       
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.commenter_name = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('blog:post_detail', year=post.publish.year, month=post.publish.month, day=post.publish.day, slug=post.slug)

    
    else:
        comment_form = CommentForm()
    context = {
            'post':post,
            'comment_form': comment_form,
            'comments':comments,
            'new_comment': new_comment,
            'similar_posts': similar_posts,
            'read_min': read_time_minutes
          
        }
    return render(request, 'post/details.html', context)






@login_required
def post_list_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])

    context = {
        'tag': tag,
        'posts': posts
    }
    return render(request, 'post/related_tags.html', context)




@login_required
def post_share(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            
        sent = True
    
    else:
        form = EmailPostForm()
    context = {
            'post':post,
            'form':form,
            'sent': sent,
        }
    return render(request, 'post/sharepost.html', context)




@login_required
def my_draft(request):
    drafts = Post.objects.filter(status='draft', author=request.user)
    return render(request, 'post/draft.html', {'drafts':drafts})

def edit_draft(request, pk):
    draft = get_object_or_404(Post, id=pk)
    draft_form = DraftForm(instance=draft)
    if request.method == 'POST':
        draft_form = DraftForm(request.POST, request.FILES, instance=draft, request=request)
        if draft_form.is_valid():
            draft_form.save()
            return redirect('/')
        
    return render(request, 'post/draftForm.html', {'form':draft_form})

@login_required
def authors(request, pk):
    author = get_object_or_404(CustomUser, pk=pk)

    author_post = Post.objects.filter(author=author, status='published')

    return render(request, 'post/author.html',{'author':author, 'author_post':author_post})




@login_required
def edit_profile(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    edit_form = UserForm(instance=user)
    if request.method == 'POST':
        edit_form = UserForm(request.POST, request.FILES, instance=user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('blog:author_profile', pk ) 
    return render(request, 'post/user_profile.html', {'edit_form':edit_form})
