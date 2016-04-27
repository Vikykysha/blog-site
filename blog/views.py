from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, UserProfile, Category
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
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
        
            
            user = user_form.save()
            
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user


            # Now we save the UserProfile model instance.
            profile.save()
            

            # Update our variable to tell the template registration was successful.
            registered = True
            

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'blog/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)
   
def profile(request):
   user = request.user
   user_id  = user.id  
   profile = UserProfile.objects.get(user_id = user_id)
   return render(request, 'blog/profile.html',{'profile':profile})

def bloggers(request):
   users = User.objects.order_by('id')
   prof = UserProfile.objects.order_by('user_id')
   paginator = Paginator(users,60)
   page = request.GET.get('page')
   try:
      users = paginator.page(page)
   except InvalidPage:
      users = paginator.page(1)
   except EmptyPage:
      users = paginator.page(paginator.num_pages)                               
   return render(request,'blog/bloggers.html',{'users':users, 'prof':prof})

def post_list(request):
   posts = Post.objects.order_by('-created_date')
   paginator = Paginator(posts,60)
   page = request.GET.get('page')
   try:
      posts = paginator.page(page)
   except InvalidPage:
      posts = paginator.page(1)
   except EmptyPage:
      posts = paginator.page(paginator.num_pages)                            
   return render(request, 'blog/post_list.html', {'posts': posts})

      
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def categories(request):
   cats = Category.objects.order_by('name')
   return render(request, 'blog/categories.html', {'cats':cats})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
   posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
   paginator = Paginator(posts,60)
   page = request.GET.get('page')
   try:
      posts = paginator.page(page)
   except InvalidPage:
      posts = paginator.page(1)
   except EmptyPage:
      posts = paginator.page(paginator.num_pages)                            
   return render(request, 'blog/post_draft_list.html', {'posts': posts})

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