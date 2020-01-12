from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Images, Profile, Comment, TotalViews
from datetime import datetime
from django.urls import reverse, reverse_lazy
from .forms import (
    PostCreateForm,
    UserLoginForm,
    UserRegistrationForm,
    ProfileEditForm,
    UserEditForm ,
    CommentForm,
    PostUpdateForm,
    ImageUpdate
    )
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse #new
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.views.generic.edit import UpdateView, DeleteView
from django.template.loader import render_to_string
from django.forms import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from taggit.models import Tag
from django.core.validators import validate_email
from django.template import RequestContext 

from django.views.decorators.http import require_POST
    


# Create your views here.


 
def post_list(request):

    post_list = Post.published.all().order_by('-updated')

    query = request.GET.get('q')
    
    if query:
        post_list = Post.published.filter(
            Q(title__icontains=query)|
            Q(author__username=query)|
            Q(body__icontains=query)


        )
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    if page is None:
        start_index = 0
        end_index = 7
    else:
        (start_index, end_index ) = proper_pagination(posts, index=4)
    page_range = list(paginator.page_range)[start_index:end_index]                   
    context = {
        'posts': posts,
        'page_range': page_range,
        
         
    }
    
    return render(request, 'blog/post_list.html', context)


# Proper pagination
def proper_pagination(posts, index):
    start_index = 0
    end_index = 7
    if posts.number > index:
        start_index = posts.number - index
        end_index = start_index + end_index
    return (start_index, end_index) 

  
def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id,slug=slug)
            

        
    if not TotalViews.objects.filter(post=post, session=request.session.session_key):
    
        view = TotalViews(post=post, ip=request.META['REMOTE_ADDR'], session=request.session.session_key)
        view.save()
    else:
        pass
    

        

        



    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    comments = Comment.objects.filter(post=post, reply=None).order_by('id')

    if request.method =="POST":
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user = request.user, content=content, reply=comment_qs)
            comment.save()



            return HttpResponseRedirect(post.get_absolute_url())
    else:

        comment_form = CommentForm() 
          

    context = {
        
        
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,
        'p': post.totalviews.count(),        
    }
    return render(request, 'blog/post_detail.html', context)

@login_required(login_url='/login/')
def like_post(request):
    if request.POST.get('action')=='post':

    #post = get_object_or_404(Post, id=request.POST.get('post_id'))
        post = get_object_or_404(Post, id=request.POST.get('id'))
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            is_liked = False

        else:
            post.likes.add(request.user)
            is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
               
    }
    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request) 
        return JsonResponse({'form': html})  

@login_required(login_url='/login/')
def post_create(request):
    if request.user.is_authenticated:
        
        ImageFormset = modelformset_factory(Images, fields=('image',), extra=1)
        common_tags = Post.tags.most_common()[:4]
        if request.method == 'POST':
            form = PostCreateForm(request.POST)
            formset = ImageFormset(request.POST or None, request.FILES or None)
            if form.is_valid() and formset.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                if post.status=='published': #check whether post is published or draft                
                    messages.success(request, "Post has been successfully published.")
                else:
                    messages.success(request, "Post has been successfully created.")
                post.save()

                for f in formset:
                    try:
                        photo = Images(post=post, image=f.cleaned_data['image'])
                        photo.save()
                    except Exception:
                        break                   
            return HttpResponseRedirect(reverse('post_list'))                             
        else:
            form = PostCreateForm()
            formset = ImageFormset(queryset=Images.objects.none())
        context = {
            'common_tags': common_tags,

            'form': form, 
            'formset': formset,
        }
        return render(request, 'blog/post_create.html', context)


    
@login_required(login_url='/login/')
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    img , _ = Images.objects.get_or_create(post_id=id)

    author = post.author.username
    if request.user.is_authenticated and request.user.username==author:    
        form =  PostUpdateForm(request.POST or None, instance=post)
        formset = ImageUpdate(request.POST or None, instance=img or None, files=request.FILES or None)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            img = formset.save(commit=False)

            post.save()        
            form.save_m2m()
            img.save()
            formset.save()
                        


        

            messages.success(request, "Post  has been successfully updated.")
   
            return redirect(post.get_absolute_url())    
           
                
            
            
            
                
                
        
    else:  
        return HttpResponse("You are not the author of this post")
    context = {
        'post': post,
        'form': form,
        'formset':formset
        
         
        
    } 
    return render(request, 'blog\post_update.html', context)





def user_login(        request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            """try:
                email = validate_email(username)
                username = User.objects.get(email=username).username
            except:
                pass"""
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "You are successfully logged in.")
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    messages.warning(request, "Wrong username or password.")                      
                    return HttpResponseRedirect(reverse_lazy('user_login'))
            else:
                messages.warning(request, "Wrong username or password.")
                return HttpResponseRedirect(reverse_lazy('user_login'))
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render( request, 'blog/login.html', context)  

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    messages.success(request, " You are successfully logout.")
    return redirect('post_list')



def validate_username(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    data ={
        'is_taken': User.objects.filter(username__iexact=username).exists(),
        'is_email': User.objects.filter(email__iexact=email).exists(),
    }
    return JsonResponse(data) 
def user_register(request):
     
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])

            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, "User is  successfully  created.")
            return redirect('user_login')
    else:
        form = UserRegistrationForm()    
    context = {
        'form':form,
    }
    return render(request, 'registration/user_register.html', context)



def validate_edit_profile(request):
    mobile_number = request.GET.get('mobile_number', None)
    data={
        'is_registerd': Profile.objects.filter(mobile__iexact=mobile_number).exists(),
    }
    return JsonResponse(data)
@login_required(login_url='/login/')
def edit_profile(request):
    Profile.objects.get_or_create(user = request.user)
    if request.method == "POST":
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Pofile  has been successfully updated.")
            return redirect('blog:display_profile')
    else:
        user_form = UserEditForm(instance = request.user)

        profile_form = ProfileEditForm(instance = request.user.profile or None)
    context = {
        'user_form': user_form,     
        'profile_form': profile_form,
    }
    return render(request, 'blog/edit_profile.html', context)



@login_required(login_url='/login/')
def display_profile(request):
    user_profiles = Profile.objects.all()
    


    return render(request, 'blog/get_user_profile.html', {'user_profiles': user_profiles})


@login_required(login_url='/login/')
def user_post_history(request, author_id):
    histories = Post.objects.filter(author_id=author_id)
    #posts = Post.objects.all(author_id)   
    context ={
        
        'histories':histories
    }
    return render(request, 'blog/post_history.html', context)
    
def archive(request, id):
    username=User.objects.get(username=request.user.username)
    today = date.today()
    one_week_ago=today-timedelta(days=7)
    if id==1:
        posts=username.blog_posts.filter(created__gte=one_week_ago)
    elif id==2:
        posts=username.blog_posts.filter(created__month=today.month)
    elif id==3:
        posts=username.blog_posts.filter(created__year=today.year)
    else:
        pass
    context={
        'posts':posts
    }
    return render(request, 'blog/filter.html', context)
   


# delete post
@login_required(login_url='/login/')
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    author = post.author.username
    
    if request.method == 'POST' and request.user.is_authenticated and request.user.username==author:
        post.delete()
        messages.success(request, "Post successfully deleted! {}".format(post.title))
        return HttpResponseRedirect(reverse_lazy("post_list"))
        
    context = {
        'post': post,
        'author': author,
    }    
    return render(request, 'blog/del_post.html', context)

        
# Post user profile

def about_post_user(request, user_id):
    abouts = Profile.objects.get(user_id=user_id)
    post = Post.published.filter(author=user_id)
    user = get_object_or_404(User, id=user_id)
    following = user.followers.all()
    

    context = {
        'abouts': abouts,
        'following': following.count(),
        'post': post.count(),

        'total_followers': abouts.total_followers()
         

    }

    return render(request, "blog/about.html", context)    

#Follow and unfollow system

@require_POST
def follow(request):

    if request.method=="POST":

        user_id = request.POST.get('id', None)
        abouts = get_object_or_404(Profile, id=user_id)
       


        if abouts.followers.filter(id=request.user.id).exists():
            abouts.followers.remove(request.user)
            is_follow=False
        

        else:
            abouts.followers.add(request.user)
            is_follow=True

    
    context = {
        'abouts':abouts,
        'total_followers': abouts.total_followers(),
        'is_follow':is_follow,


               
    }
    html = render_to_string("blog/follow.html", context, request=request)
    return JsonResponse({'form':html})

    

    #return HttpResponse(json.dumps(context), content_type='application/json')


  
#Tags
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug) 
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    } 
    return render(request, 'blog/post_list.html', context)


             
def followers_following_list(request):
    profilie = get_object_or_404(Profile, id=request.user.id)
    followers = profilie.followers.all()
    user = get_object_or_404(User, id=request.user.id)
    followings = user.followers.all()
        
    
    context ={
        'followings': followings,
        
        
        'followers':followers,
    }


    return render(request, "blog/followers_following.html", context)


    
        



                
    




    
