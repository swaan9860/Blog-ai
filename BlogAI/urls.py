# BlogAI/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # Added import
from moderation.admin import moderation_admin_site  # Import custom admin site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/moderation/', moderation_admin_site.urls, name='moderation_admin'),  # Custom admin site
    path('', include('blog.urls')),  # Add this to map root URL to blog app
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)