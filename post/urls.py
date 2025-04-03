from django.urls import path
from . import views
urlpatterns = [
    path('<int:pk>/',views.PostDetail.as_view(), name='post-detail'),
    path('home/',views.HomePostList.as_view()),
    #path('',views.PostList.as_view()),
    path('userbloglist',views.UserBlogList.as_view(),name='userbloglist'),
    #list of all authors
   # path('authorsall',views.all_authors,name='authorsall'),
    path('all-authorpost/<int:pk>/',views.ListAuthorPost.as_view(), name='all-authorpost'),
    path('like-post/<int:pk>/',views.likePost, name='like-post'),
    path('postcomment/<int:pk>/',views.postcomment, name='postcomment'),

    ## newest post
    path('newest-post',views.newest_post,name='newest-post'),
    ## create post
    path('create-post/',views.createpost,name='create-post'),

]
