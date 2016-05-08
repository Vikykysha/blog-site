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

def register(request):
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
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)
   
def profile(request):
   tags = Tag.objects.all()
   user = request.user
   user_id  = user.id  
   profile = UserProfile.objects.get(user_id = user_id)
   return render(request, 'blog/profile.html',{'profile':profile,'tags':tags})

def bloggers(request):
   tags = Tag.objects.all()
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
def like_category(request,pk):
   
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        post_pk = post.pk
        post_p = post.addLike
    likes = 0
    if post_pk and (post_p==0):
        post = Post.objects.get(pk=(int(post_pk)))
        if post:
            likes = post.likes + 1
            post.likes =  likes
            l = post.addLike + 1
            post.addLike = l
            post.save()
            

    return redirect('blog.views.post_detail', pk=pk)

def post_list(request):
   tags = Tag.objects.all()
   posts = Post.objects.order_by('-created_date')
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
    tags = Tag.objects.all()
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post,'tags':tags})

def categories(request):
   tags = Tag.objects.all()
   cats = Category.objects.order_by('name')
   return render(request, 'blog/categories.html', {'cats':cats,'tags':tags})

@login_required
def post_new(request):
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
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
   tags = Tag.objects.all()
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
    return render(request, 'blog/post_edit.html', {'form': form})

def add_comment_to_post(request, pk):
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
    return render(request, 'blog/add_comment_to_post.html', {'form': form})



   

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