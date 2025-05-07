# BlogAI/moderation/admin.py
from django.contrib import admin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.urls import reverse
from django.utils.html import format_html
from .models import FlaggedContent

@admin.register(FlaggedContent)
class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ['post_title', 'user', 'reason', 'score', 'content_preview', 'flagged_at', 'is_approved']
    list_filter = ['is_approved', 'reason', 'flagged_at']
    search_fields = ['post__title', 'user__username', 'reason']
    actions = ['approve_content', 'reject_content']
    list_per_page = 25

    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = 'Post Title'
    post_title.admin_order_field = 'post__title'

    def content_preview(self, obj):
        post_url = reverse('admin:blog_post_change', args=[obj.post.id])
        preview = obj.post.content[:100] + ('...' if len(obj.post.content) > 100 else '')
        return format_html('<a href="{}">{}</a>', post_url, preview)
    content_preview.short_description = 'Content Preview'

# BlogAI/moderation/admin.py (relevant action methods)
def approve_content(self, request, queryset):
    for flag in queryset:
        if not flag.is_approved:
            flag.is_approved = True
            flag.post.is_published = True
            flag.post.save()
            flag.save()
            try:
                send_mail(
                    subject='Your Post Has Been Approved',
                    message=f'Your post "{flag.post.title}" has been approved and is now published.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[flag.user.email],
                    fail_silently=True
                )
            except Exception as e:
                messages.warning(request, f'Failed to notify user {flag.user.username}: {str(e)}')
    messages.success(request, f'{queryset.count()} post(s) approved and published.')
approve_content.short_description = "Approve and publish selected content"

def reject_content(self, request, queryset):
    for flag in queryset:
        post = flag.post
        flag.delete()
        post.delete()
        try:
            send_mail(
                subject='Your Post Has Been Rejected',
                message=f'Your post "{post.title}" was rejected due to inappropriate content: {flag.reason}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[flag.user.email],
                fail_silently=True
            )
        except Exception as e:
            messages.warning(request, f'Failed to notify user {flag.user.username}: {str(e)}')
    messages.success(request, f'{queryset.count()} post(s) rejected and deleted.')
reject_content.short_description = "Reject and delete selected content"

# Custom Admin Dashboard for Moderation
class ModerationAdminSite(admin.AdminSite):
    site_header = 'Blog Platform Moderation Dashboard'
    site_title = 'Moderation Dashboard'
    index_title = 'Moderation Overview'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.moderation_dashboard), name='moderation_dashboard'),
        ]
        return custom_urls + urls

    @permission_required('moderation.view_flaggedcontent')
    def moderation_dashboard(self, request):
        flagged_count = FlaggedContent.objects.count()
        pending_count = FlaggedContent.objects.filter(is_approved=False).count()
        approved_count = FlaggedContent.objects.filter(is_approved=True).count()
        context = {
            'flagged_count': flagged_count,
            'pending_count': pending_count,
            'approved_count': approved_count,
            'recent_flags': FlaggedContent.objects.order_by('-flagged_at')[:5],
        }
        return render(request, 'admin/moderation_dashboard.html', context)

# Register the custom admin site
moderation_admin_site = ModerationAdminSite(name='moderation_admin')
moderation_admin_site.register(FlaggedContent, FlaggedContentAdmin)