from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('signup/', views.signup, name='signup'),
    
    # Authentication URLs with custom templates
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='registration/login.html',
             redirect_authenticated_user=True
         ), 
         name='login'),
    
    path('logout/', views.logout_user, name='logout'),
    
    # Optional: Password reset URLs
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'
         ),
         name='password_reset'),
    
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    # Your other URLs
    path('search/', views.search_posts, name='search_posts'),
    path('profile/', views.profile_settings, name='profile_settings'),
    path('my-posts/', views.user_posts, name='user_posts'),
    # path('ajax/search/', views.ajax_search, name='ajax_search'),
]