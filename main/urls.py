from django.urls import path
from .views import *

urlpatterns = [
    path('',BlogPostListView.as_view(),name='blog-list'),
    path('blog/create/',BlogPostCreateView.as_view(),name='blog-create'),
    
    path('blog/<int:post_id>/',BlogReadView.as_view(),name='blog'),
    path('my-blog/',UserBlogListView.as_view(),name='my-blog'),
    path('my-blog/<int:post_id>/update/',BlogUpdateView.as_view(),name='update-blog'),
    path('my-blog/<int:post_id>/delete/',BlogDeleteView.as_view(),name='delete-blog'),
    path('likes/<int:post_id>/',LikePostView.as_view(),name='like-post'),
    path('dislikes/<int:post_id>/',DislikePostView.as_view(),name='dislike-post'),
    path('comment_likes/<int:comment_id>/',CommentLikePostView.as_view(),name='comment-like-post'),
    path('comment_dislikes/<int:comment_id>/',CommentDislikePostView.as_view(),name='comment-dislike-post'),
    path('interest/',InterestPostView.as_view(),name="interest_post"),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('select-interest/<int:id>/', SelectInterestView.as_view(), name='select_interest'),
    path('my-interests/', UserInterestListView.as_view(), name='user-interests'),
    path("follow/<int:id>/",FollowPostView.as_view(),name='follow'),
    path('blog/following/',UserFollowListView.as_view(),name='following-blog'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('profile/update/',UpdateProfileView.as_view(),name='profile-update'),
 
]
