from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, UserProfile, Category, Tag
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from blog.forms import UserForm, UserProfileForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
import json

def tag_json(request):
    tag = list(Tag.objects.values_list('name', flat=True))
    
    

    return HttpResponse(json.dumps(tag),  content_type="application/json")

def register(request):
    tagss = Tag.objects.all()
    posts = Post.objects.order_by('-created_date')
   
    for tag in tagss:
       q = Post.objects.filter(tags=tag)
       z = q.count()>2
       if z:
          x=True
          tag.important=x
          tag.save()
    tags=Tag.objects.filter(important=True)
    # Like before, get the request's context.
    
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
               
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True                  
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response(
            'blog/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered,'tags':tags},
            context)
   
def profile(request):
   tagss = Tag.objects.all()
   posts = Post.objects.order_by('-created_date')
   
   for tag in tagss:
      q = Post.objects.filter(tags=tag)
      z = q.count()>2
      if z:
         x=True
         tag.important=x
         tag.save()
   tags=Tag.objects.filter(important=True)
   user = request.user
   user_id  = user.id  
   profile = UserProfile.objects.get(user_id = user_id)
   return render(request, 'blog/profile.html',{'profile':profile,'tags':tags})

def bloggers(request):
   tagss = Tag.objects.all()
   posts = Post.objects.order_by('-created_date')
   
   for tag in tagss:
      q = Post.objects.filter(tags=tag)
      z = q.count()>2
      if z:
         x=True
         tag.important=x
         tag.save()
   tags=Tag.objects.filter(important=True)
   users = User.objects.order_by('id')
   prof = UserProfile.objects.order_by('user_id')
   list = zip(users, prof)
   paginator = Paginator(users,60)
   page = request.GET.get('page')
   try:
      users = paginator.page(page)
   except InvalidPage:
      users = paginator.page(1)
   except EmptyPage:
      users = paginator.page(paginator.num_pages)                               
   return render(request,'blog/bloggers.html',{'users':users, 'prof':prof, 'list':list,'tags':tags})

@login_required
def like_category(request):

    pk = None
    if request.method == 'GET':
        pk = request.GET['post_pk']

    
    if pk:
        post = Post.objects.get(pk=(int(pk)))
        if post:
            likes = post.likes + 1
            post.likes =  likes
            post.save()

    return HttpResponse(likes)



@login_required
def dislike_category(request):

    pk = None
    if request.method == 'GET':
        pk = request.GET['post_pk']

    
    if pk:
        post = Post.objects.get(pk=(int(pk)))
        if post:
            dislikes = post.dislikes + 1
            post.dislikes =  dislikes
            post.save()

    return HttpResponse(dislikes)

@login_required
def down(request):

    pk = None
    if request.method == 'GET':
        pk = request.GET['post_pk']

    
    if pk:
        post = Post.objects.get(pk=(int(pk)))
        if post:
            dislikes = post.dislikes - 1
            post.dislikes =  dislikes
            post.save()

    return HttpResponse(dislikes)
@login_required
def downl(request):

    pk = None
    if request.method == 'GET':
        pk = request.GET['post_pk']

    
    if pk:
        post = Post.objects.get(pk=(int(pk)))
        if post:
            likes = post.likes - 1
            post.likes =  likes
            post.save()

    return HttpResponse(likes)





def post_list(request):
   tagss = Tag.objects.all()
   posts = Post.objects.order_by('-created_date')
   
   for tag in tagss:
      q = Post.objects.filter(tags=tag)
      z = q.count()>2
      if z:
         x=True
         tag.important=x
         tag.save()
   tags=Tag.objects.filter(important=True)
   paginator = Paginator(posts,60)
   page = request.GET.get('page')
   try:
      posts = paginator.page(page)
   except InvalidPage:
      posts = paginator.page(1)
   except EmptyPage:
      posts = paginator.page(paginator.num_pages)                            
   return render(request, 'blog/post_list.html', {'posts': posts,'tags':tags})

      
def post_detail(request, pk):
    tagss = Tag.objects.all()
    posts = Post.objects.order_by('-created_date')
   
    for tag in tagss:
       q = Post.objects.filter(tags=tag)
       z = q.count()>2
       if z:
          x=True
          tag.important=x
          tag.save()
    tags=Tag.objects.filter(important=True)
    post = get_object_or_404(Post, pk=pk)
    gl = post.glance + 1
    post.glance = gl
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post,'tags':tags})

def categories(request):
   tagss = Tag.objects.all()
   posts = Post.objects.order_by('-created_date')
   
   for tag in tagss:
      q = Post.objects.filter(tags=tag)
      z = q.count()>2
      if z:
         x=True
         tag.important=x
         tag.save()
   tags=Tag.objects.filter(important=True)
   cats = Category.objects.order_by('name')
   return render(request, 'blog/categories.html', {'cats':cats,'tags':tags})

@login_required
def post_new(request):
    tagss = Tag.objects.all()
    posts = Post.objects.order_by('-created_date')
   
    for tag in tagss:
      q = Post.objects.filter(tags=tag)
      z = q.count()>2
      if z:
         x=True
         tag.important=x
         tag.save()
    tags=Tag.objects.filter(important=True)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["tags"]: 
               ta = Tag.objects.filter(name=form.cleaned_data["tags"])
               if ta.exists():
                  ta = Tag.objects.get(name=form.cleaned_data["tags"])
                  ta.save()
                  post=Post.objects.create(author = request.user,title=form.cleaned_data["title"],text=form.cleaned_data["text"],category=form.cleaned_data["category"])
                  post.save()
                  post.tags.add(ta)
               else:  
                  t=Tag.objects.create(name=form.cleaned_data["tags"])
                  t.save()
                  post=Post.objects.create(author = request.user,title=form.cleaned_data["title"],text=form.cleaned_data["text"],category=form.cleaned_data["category"])
                  post.save()
                  post.tags.add(t)
                
            else:
               post=Post.objects.create(author = request.user,title=form.cleaned_data["title"],text=form.cleaned_data["text"],category=form.cleaned_data["category"])
        
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form,'tags':tags})

@login_required
def post_draft_list(request):
   tagss = Tag.objects.all()
   posts = Post.objects.order_by('-created_date')
   
   for tag in tagss:
      q = Post.objects.filter(tags=tag)
      z = q.count()>2
      if z:
         x=True
         tag.important=x
         tag.save()
   tags=Tag.objects.filter(important=True)
   posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
   paginator = Paginator(posts,60)
   page = request.GET.get('page')
   try:
      posts = paginator.page(page)
   except InvalidPage:
      posts = paginator.page(1)
   except EmptyPage:
      posts = paginator.page(paginator.num_pages)                            
   return render(request, 'blog/post_draft_list.html', {'posts': posts,'tags':tags})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)
   
@login_required   
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog.views.post_list')

@login_required
def post_edit(request, pk):
    tagss = Tag.objects.all()
    posts = Post.objects.order_by('-created_date')
   
    for tag in tagss:
       q = Post.objects.filter(tags=tag)
       z = q.count()>2
       if z:
          x=True
          tag.important=x
          tag.save()
    tags=Tag.objects.filter(important=True)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form,'tags':tags})

def add_comment_to_post(request, pk):
    tagss = Tag.objects.all()
    posts = Post.objects.order_by('-created_date')
   
    for tag in tagss:
       q = Post.objects.filter(tags=tag)
       z = q.count()>2
       if z:
          x=True
          tag.important=x
          tag.save()
    tags=Tag.objects.filter(important=True)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form,'tags':tags})



   

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)


def tag(request,name) :
   
   
   tags = Tag.objects.all()
   tag_s= Tag.objects.get(name=name)
   posts= Post.objects.filter(tags__exact=tag_s)
   paginator = Paginator(posts,60)
   page = request.GET.get('page')
   try:
      posts = paginator.page(page)
   except InvalidPage:
      posts = paginator.page(1)
   except EmptyPage:
      posts = paginator.page(paginator.num_pages)                    
   return render(request, 'blog/tags.html',{'posts':posts,'tag':tag_s,'tags':tags})