from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404



class BlogPostCreateView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        form=BlogPostForm()
        return render(request,'main/create_post.html',{'form':form,'username':request.user.username})
    
    
    def post(self,request,*args,**kwargs):
        form = BlogPostForm(request.POST)
        
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('my-blog')
        
        return render(request,"main/create_post.html",{'form':form,'username':request.user.username})

class InterestPostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            profile = user.profile
            user_topic = profile.interests.all()
            if user_topic.exists():
                interested = BlogPost.objects.filter(category__in=user_topic).exclude(author=user).distinct()
            else:
                interested = BlogPost.objects.none() 
        except Profile.DoesNotExist:
            raise Http404("Profile not found. Please create a profile.")
        
        paginator = Paginator(interested, 6)  
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "main/interest_post.html", {'interested_post': page_obj})

class UserInterestListView(LoginRequiredMixin, View):
    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        interests = profile.interests.all()
        return render(request, 'main/interest_list.html', {'interests': interests})

class CategoryListView(View):
    template_name = 'main/category_list.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all() 
        context = {'categories': categories}  
        return render(request, self.template_name, context)
        
class SelectInterestView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        category=get_object_or_404(Category,id=kwargs['id'])
        profile = request.user.profile
        
        if category in profile.interests.all():
            profile.interests.remove(category)
        else:
            profile.interests.add(category)

        return redirect(request.META.get("HTTP_REFERER", "/"))
    
class FollowPostView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        author=get_object_or_404(User,id=kwargs['id'])
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        
        if author.profile in user_profile.following.all():
            user_profile.following.remove(author.profile)
        else:
            user_profile.following.add(author.profile)
            
        return redirect(request.META.get('HTTP_REFERER', 'blog-list'))
            
    
class LikePostView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        blogpost=get_object_or_404(BlogPost,id=kwargs['post_id'])
        
        if request.user in blogpost.likes.all():
            blogpost.likes.remove(request.user)
        
        else:
            blogpost.likes.add(request.user)
            if request.user in blogpost.dislikes.all():
                blogpost.dislikes.remove(request.user)
        blogpost.save()
        return redirect('blog',post_id=kwargs['post_id'])

class DislikePostView(LoginRequiredMixin,View):
    def post(self,request,post_id,*args,**kwargs):
        blogpost=get_object_or_404(BlogPost,id=post_id)
        
        if request.user in blogpost.dislikes.all():
            blogpost.dislikes.remove(request.user)
        
        else:
            blogpost.dislikes.add(request.user)
            if request.user in blogpost.likes.all():
                blogpost.likes.remove(request.user)
        blogpost.save() 
        return redirect('blog',post_id=post_id)
    

class CommentLikePostView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        comment=get_object_or_404(Comment,id=kwargs['comment_id'])
        blogpost = comment.post
        if request.user in comment.comment_likes.all():
            comment.comment_likes.remove(request.user)
        
        else:
            comment.comment_likes.add(request.user)
            if request.user in comment.comment_dislikes.all():
                comment.comment_dislikes.remove(request.user)
            
        return redirect('blog',post_id=blogpost.id)

class CommentDislikePostView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        comment=get_object_or_404(Comment,id=kwargs['comment_id'])
        blogpost = comment.post
        if request.user in comment.comment_dislikes.all():
            comment.comment_dislikes.remove(request.user)
        
        else:
            comment.comment_dislikes.add(request.user)
            comment.comment_likes.remove(request.user)
            
        return redirect('blog',post_id=blogpost.id)

class BlogPostListView(View):
    def get(self,request,*args,**kwargs):
        query=request.GET.get("queries","")
        if query:
            blogpost=BlogPost.objects.filter(
                Q(blog_title__icontains=query) |
                Q(author__username__icontains=query)
            ).order_by("-created_at")
        else:
            blogpost=BlogPost.objects.all().order_by('-created_at')
        paginator=Paginator(blogpost,6)
        page_num=request.GET.get("page")
        blogposts=paginator.get_page(page_num)
        return render(request,'main/blog_list.html',{'blogposts':blogposts})

class BlogReadView(View):
    def get(self, request, *args, **kwargs):
        blogpost = get_object_or_404(BlogPost, id=kwargs['post_id'])
        comments = blogpost.posts_comments.filter(parent__isnull=True).order_by("-created_at")
        form = CommentForm()
        return render(request, 'main/blog.html', {'blogpost': blogpost, 'comments': comments, 'form': form})
    
    def post(self, request, *args, **kwargs):
        blogpost = get_object_or_404(BlogPost, id=kwargs['post_id'])
        form = CommentForm(request.POST)
        parent_id = request.POST.get('parent_id')
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blogpost
            if request.user.is_authenticated:
                comment.user = request.user
                comment.guest_name = None 
            else:
                comment.guest_name = request.POST.get('guest_name') 
                comment.user=None

            if parent_id:
                parent_comment = Comment.objects.filter(id=parent_id).first()
                comment.parent = parent_comment

            comment.save()
            
            if blogpost.author != comment.user:
                send_mail(
                    subject=f"New comment on {blogpost.blog_title}",
                    message=f"{comment.user.username if comment.user else comment.guest_name } commented on your blog post.\n\n Comment: '{comment.content}.'",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[blogpost.author.email],
                    fail_silently=True
                )
            
            if parent_id:
                parent_comment=Comment.objects.filter(id=parent_id).first()
                if parent_comment and parent_comment.user != comment.user:
                    send_mail(
                    subject=f"New Reply on {blogpost.blog_title}",
                    message=f"{comment.user.username if comment.user else comment.guest_name } commented on your blog post.\n\n Comment: '{comment.content}.'",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[blogpost.author.email],
                    fail_silently=True
                )
                
            return redirect('blog', post_id=blogpost.id)
        
        comments = blogpost.posts_comments.filter(parent__isnull=True).order_by("-created_at")
        return render(request, 'main/blog.html', {'blogpost': blogpost, 'form': form, 'comments': comments})

class BlogUpdateView(View):
    def get(self,request,*args,**kwargs):
        blogpost=get_object_or_404(BlogPost,id=kwargs['post_id'])
        form=BlogPostForm(instance=blogpost)
        return render(request,"main/create_post.html",{'form':form,'username':request.user.username})
    
    def post(self,request,*args,**kwargs):
        blogpost=get_object_or_404(BlogPost,id=kwargs['post_id'])
        form=BlogPostForm(request.POST,instance=blogpost)
        if form.is_valid():
            update_post=form.save(commit=False)
            update_post.author=request.user
            update_post.save()
            return redirect("my-blog")
        return render(request,"main/create_post.html",{'form':form,'username':request.user.username})
    
class BlogDeleteView(View):
    def get(self,request,*args,**kwargs):
        blogpost=get_object_or_404(BlogPost,id=kwargs['post_id'])
        return render(request, "main/confirm_delete.html",{'blogposts':blogpost})
    def post(self,request,*args,**kwargs):
        blogpost=get_object_or_404(BlogPost,id=kwargs['post_id'])
        blogpost.delete()
        return redirect('my-blog')


class UserBlogListView(View):
    def get(self,request,*args,**kwargs):
        blogpost=BlogPost.objects.filter(author=request.user).order_by('-created_at')
        paginator=Paginator(blogpost,6)
        page_num=request.GET.get("page")
        blogposts=paginator.get_page(page_num)
        total_pages=blogposts.paginator.num_pages
        return render(request,'main/user_post_list.html',{'blogposts':blogposts,'total_page':total_pages})

class UserFollowListView(View):
    def get(self,request,*args,**kwargs):
        profile=request.user.profile
        following_user_id=profile.following.values_list('user',flat=True)
        blogpost=BlogPost.objects.filter(author__in=following_user_id).order_by('-created_at')
        pagination=Paginator(blogpost,6)
        page_num=request.GET.get('page')
        blogposts=pagination.get_page(page_num)
        return render(request,'main/follow_bloglist.html',{'blogposts':blogposts})

class UserProfileView(View):
    def get(self,request,*args,**kwargs):
        profile=get_object_or_404(Profile,user=request.user)
        
        return render(request,'main/profile.html',{'profile':profile})

class UpdateProfileView(View):
    def get(self,request,*args,**kwargs):
        user=request.user
        profile=user.profile
        user_form=UpdateuserForm(instance=user)
        profile_form=UpdateProfileForm(instance=profile)
        return render(request,'main/update_profile.html',{'user_form':user_form,'profile_form':profile_form})
    
    def post(self,request,*args,**kwargs):
        user=request.user
        profile=user.profile
        user_form=UpdateuserForm(request.POST,request.FILES,instance=user)
        profile_form=UpdateProfileForm(request.POST,request.FILES,instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
            
        return render(request,"main/update_profile.html",{'user_form':user_form,'profile_form':profile_form})