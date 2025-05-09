from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('signup/', views.signup, name='signup'),
    path('preferences/', views.user_preferences, name='user_preferences'),
    path('search/', views.search_posts, name='search_posts'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.user_settings, name='user_settings'),
    path('my-posts/', views.user_posts, name='user_posts'),
    path('ajax/search/', views.ajax_search, name='ajax_search'),
    path('logout/', views.logout_user, name='logout'),
]
