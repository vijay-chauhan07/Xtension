"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings

from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from blog import views
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
 



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.post_list, name='post_list'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('login/', views.user_login , name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('edit/profile/', views.edit_profile, name='edit_profile'),
    path('ajax/mobile/number/validator', views.validate_edit_profile, name='validate_edit_profile'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('register/', views.user_register, name='user_register'),
    #Password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('<int:user_id>/', views.about_post_user, name='about_post_user'),
    path('like/', views.like_post, name='like_post'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('<slug>/', views.tagged, name='tagged'),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

