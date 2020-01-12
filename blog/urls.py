from django.urls import path

from django.conf.urls import url


from . import views

app_name = 'blog'
urlpatterns = [
     
    
    path('<int:id>/<slug>/detail', views.post_detail, name='post_detail'),
    path('new/', views.post_create, name='post_create'),
    path('logout/', views.user_logout, name='user_logout'),
    #path('<int:pk>/updated-post', views.PostUpdateView.as_view(), name='post_update'),
    #path('<int:pk>/deleted-post', views.PostDeleteView.as_view(), name='post_delete'),
    path('profile/', views.display_profile, name='display_profile'),
    path('<int:author_id>/post/history/', views.user_post_history, name='user_post_history'),
    path('post/<int:id>/update/', views.post_update, name='post_update'),
    path('<int:id>/delete/', views.post_delete, name='delete'),
    path('<int:id>/archive/', views.archive, name='archive'),
    path('profile/follow/', views.follow, name='user_follow'),
    path("user/followers_following_list/", views.followers_following_list, name="followers_following_list"),
    
    
    
]