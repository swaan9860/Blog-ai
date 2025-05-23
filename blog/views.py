from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Post, Profile, UserPreference, PostInteraction, UserProfile
from .forms import PostForm, CommentForm, ProfileForm, UserPreferenceForm, AvatarUploadForm, UserUpdateForm
from moderation.models import FlaggedContent
from moderation.utils import moderate_content
from moderation.keyword_moderation import moderate_keywords
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity

User = get_user_model()

def home(request):
    recent_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    no_posts_message = "No posts available. Be the first to share!" if not recent_posts else None
    recommended_posts = None
    if request.user.is_authenticated:
        try:
            recommended_posts = get_collaborative_recommendations(request.user)
            if not recommended_posts:
                user_prefs = request.user.userpreference
                preferred_tags = user_prefs.preferred_tags.names()
                if preferred_tags:
                    recommended_posts = Post.objects.filter(
                        tags__name__in=preferred_tags
                    ).exclude(author=request.user).distinct()[:3]
        except UserPreference.DoesNotExist:
            pass
    return render(request, 'blog/home.html', {
        'recent_posts': recent_posts,
        'no_posts_message': no_posts_message,
        'recommended_posts': recommended_posts
    })

def post_list(request):
    query = request.GET.get('q', '')
    posts = Post.objects.exclude(slug__exact='')
    if request.user.is_authenticated:
        posts = posts.filter(Q(is_published=True) | Q(author=request.user))
    else:
        posts = posts.filter(is_published=True)
    posts = posts.order_by('-created_at')
    recommended_posts = None
    if request.user.is_authenticated:
        try:
            recommended_posts = get_collaborative_recommendations(request.user)
            if not recommended_posts:
                user_prefs = request.user.userpreference
                preferred_tags = user_prefs.preferred_tags.names()
                if preferred_tags:
                    recommended_posts = Post.objects.filter(
                        tags__name__in=preferred_tags
                    ).exclude(author=request.user).distinct()[:3]
        except UserPreference.DoesNotExist:
            pass
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__in=[query])
        ).distinct()
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'query': query,
        'recommended_posts': recommended_posts
    })

def search_suggestions(request):
    query = request.GET.get('term', '').strip()
    if query:
        tags = Post.objects.filter(
            tags__name__istartswith=query
        ).values_list('tags__name', flat=True).distinct()[:10]
        suggestions = list(set(tags))
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)

def ajax_search(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.exclude(slug__exact='')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__in=[query])
        ).distinct()[:10]
    results = [{
        'title': post.title,
        'slug': post.slug,
        'content': post.content[:100],
        'author': post.author.username,
        'created_at': post.created_at.strftime('%b %d, Y'),
        'picture': post.picture.url if post.picture else None
    } for post in posts]
    return JsonResponse({'results': results})

def get_collaborative_recommendations(user, num_recommendations=3):
    users = User.objects.all()
    posts = Post.objects.filter(is_published=True)
    if not users or not posts:
        return None
    user_ids = {user.id: idx for idx, user in enumerate(users)}
    post_ids = {post.id: idx for idx, post in enumerate(posts)}
    rows, cols, data = [], [], []
    interactions = PostInteraction.objects.filter(viewed=True)
    for interaction in interactions:
        if interaction.user.id in user_ids and interaction.post.id in post_ids:
            rows.append(user_ids[interaction.user.id])
            cols.append(post_ids[interaction.post.id])
            data.append(1)
    interaction_matrix = coo_matrix((data, (rows, cols)), shape=(len(users), len(posts)))
    interaction_matrix = interaction_matrix.tocsr()
    similarity = cosine_similarity(interaction_matrix)
    user_idx = user_ids.get(user.id)
    if user_idx is None:
        return None
    similar_users = np.argsort(similarity[user_idx])[::-1][1:11]
    similar_user_ids = [list(user_ids.keys())[idx] for idx in similar_users]
    viewed_posts = set(PostInteraction.objects.filter(user=user, viewed=True).values_list('post__id', flat=True))
    recommended_posts = Post.objects.filter(
        postinteraction__user__id__in=similar_user_ids,
        postinteraction__viewed=True
    ).exclude(id__in=viewed_posts).distinct()[:num_recommendations]
    return recommended_posts

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        PostInteraction.objects.get_or_create(user=request.user, post=post, defaults={'viewed': True})
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            text_to_moderate = f"{post.title} {post.content}"
            ai_flagged, ai_score, ai_reason = moderate_content(text_to_moderate)
            kw_flagged, kw_score, kw_reason = moderate_keywords(text_to_moderate)
            try:
                ai_score = float(ai_score) if ai_score is not None else 0.0
                kw_score = float(kw_score) if kw_score is not None else 0.0
            except (ValueError, TypeError):
                kw_score = 0.0
                ai_score = 0.0
            if ai_flagged or kw_flagged:
                post.is_published = False
                post.save()
                form.save_m2m()
                reason = f"{ai_reason}; {kw_reason}" if ai_flagged and kw_flagged else (ai_reason if ai_flagged else kw_reason)
                score = max(ai_score, kw_score)
                FlaggedContent.objects.create(
                    post=post,
                    user=request.user,
                    reason=reason,
                    score=score
                )
                messages.warning(request, 'Post flagged for review due to potential inappropriate content.')
                return redirect('post_list')
            base_slug = slugify(post.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug
            post.is_published = True
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created!')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden("You can only edit your own posts.")
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            text_to_moderate = f"{updated_post.title} {updated_post.content}"
            try:
                # AI-based moderation
                ai_flagged, ai_score, ai_reason = moderate_content(text_to_moderate)
                # Keyword-based moderation
                kw_flagged, kw_matches, kw_score = moderate_keywords(text_to_moderate)
                ai_score = float(ai_score) if ai_score is not None else 0.0
                kw_score = float(kw_score) if kw_score is not None else 0.0
                if ai_flagged or kw_flagged:
                    # Flag the post
                    updated_post.is_published = False
                    updated_post.save()
                    form.save_m2m()
                    reason = f"{ai_reason}; Inappropriate phrase: {', '.join(kw_matches)}" if ai_flagged and kw_flagged else (ai_reason if ai_flagged else f"Inappropriate phrase: {', '.join(kw_matches)}")
                    score = max(ai_score, kw_score)
                    # Create or update FlaggedContent
                    FlaggedContent.objects.update_or_create(
                        post=updated_post,
                        user=request.user,
                        defaults={'reason': reason, 'score': score}
                    )
                    messages.warning(request, f'Post flagged for review due to potential inappropriate content (Score: {score})')
                    return redirect('post_list')
                else:
                    # Unflag the post
                    updated_post.is_published = True
                    updated_post.save()
                    form.save_m2m()
                    # Remove any existing FlaggedContent
                    FlaggedContent.objects.filter(post=updated_post, user=request.user).delete()
                    messages.success(request, 'Post updated and cleared of any flags!')
                    return redirect(post.get_absolute_url())
            except Exception as e:
                messages.error(request, f'Error during moderation: {str(e)}')
                return render(request, 'blog/post_edit.html', {'form': form, 'post': post})
        else:
            messages.error(request, 'Form validation failed. Please check your inputs.')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author.username != request.user.username:
        return HttpResponseForbidden("You can only delete your own posts.")
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted!')
        return redirect('post_list')
    return render(request, 'blog/post_delete.html', {'post': post})

@login_required
def user_preferences(request):
    try:
        preference = request.user.userpreference
    except UserPreference.DoesNotExist:
        preference = UserPreference(user=request.user)
        preference.save()
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferences updated!')
            return redirect('post_list')
    else:
        form = UserPreferenceForm(instance=preference)
    return render(request, 'blog/preferences.html', {'form': form})

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AvatarUploadForm(instance=user_profile)
    return render(request, 'blog/profile.html', {'form': form})

@login_required
def user_settings(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        if 'avatar_submit' in request.POST:
            avatar_form = AvatarUploadForm(request.POST, request.FILES, instance=user_profile)
            user_form = UserUpdateForm(instance=request.user)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, 'Avatar updated!')
                return redirect('user_settings')
        elif 'profile_submit' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            avatar_form = AvatarUploadForm(instance=user_profile)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated!')
                return redirect('user_settings')
    else:
        avatar_form = AvatarUploadForm(instance=user_profile)
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'blog/user_settings.html', {
        'avatar_form': avatar_form,
        'user_form': user_form
    })

@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/user_posts.html', {'posts': posts})

def search_posts(request):
    query = request.GET.get('q', '')
    posts = []
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).filter(is_published=True).distinct()
    
    context = {
        'query': query,
        'posts': posts,
    }
    return render(request, 'blog/search_results.html', context)

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')