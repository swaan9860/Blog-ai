# blog/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.core.cache import cache  # For sentiment caching

from .models import Post, UserPreference, PostInteraction, UserProfile, Comment
from .forms import PostForm, UserPreferenceForm, AvatarUploadForm, UserUpdateForm, CommentForm

from moderation.utils import moderate_content, get_post_sentiment_score
from moderation.models import FlaggedContent

User = get_user_model()


def home(request):
    recommended_posts = []
    if request.user.is_authenticated:
        recommended_posts = get_recommendations(request.user)

    context = {
        'recommended_posts': recommended_posts,
    }
    return render(request, 'blog/home.html', context)


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    
    # Optional: Attach sentiment scores if you want to display them
    posts_with_sentiment = []
    for post in posts:
        score = get_post_sentiment_score_with_cache(post)
        posts_with_sentiment.append({
            'post': post,
            'sentiment_score': score,
        })

    recommended_posts = []
    if request.user.is_authenticated:
        recommended_posts = get_recommendations(request.user)

    context = {
        'posts_with_sentiment': posts_with_sentiment,
        'recommended_posts': recommended_posts,
    }
    return render(request, 'blog/post_list.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            full_text = f"{post.title} {post.content}"
            is_flagged, reason, score = moderate_content(full_text)

            if is_flagged:
                post.is_published = False
                FlaggedContent.objects.create(
                    post=post,
                    reason=reason or "Content violation",
                    score=score or 1.0
                )
                messages.warning(
                    request,
                    "Your post has been flagged for review and is not visible to others."
                )
            else:
                post.is_published = True
                messages.success(request, "Your post has been published successfully!")

            post.save()
            form.save_m2m()  # Save tags
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'blog/post_create.html', {'form': form})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Hide unpublished posts from non-authors
    if not post.is_published and request.user != post.author:
        return render(request, '404.html')

    # Record view for recommendations
    if request.user.is_authenticated:
        PostInteraction.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={'viewed': True}
        )

    # Fetch top-level comments with prefetched replies
    comments = post.comments.filter(parent=None).prefetch_related(
        'replies__author',
        'replies__replies__author',
        'author'
    )

    # Handle new comment/reply
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    comment.parent = Comment.objects.get(id=parent_id, post=post)
                except Comment.DoesNotExist:
                    messages.error(request, "Invalid reply target.")
                    return redirect('post_detail', slug=slug)

            comment.save()
            messages.success(request, "Your comment has been posted!")
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    was_published_before = post.is_published

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)

            full_text = f"{updated_post.title} {updated_post.content}"
            is_flagged, reason, score = moderate_content(full_text)

            # Remove any previous flags
            FlaggedContent.objects.filter(post=updated_post).delete()

            if is_flagged:
                updated_post.is_published = False
                FlaggedContent.objects.create(
                    post=updated_post,
                    reason=reason or "Content violation",
                    score=score or 1.0
                )
                messages.warning(
                    request,
                    f"Post updated but flagged: {reason} (score: {score:.2f}). It remains under review."
                )
            else:
                updated_post.is_published = True
                if not was_published_before:
                    messages.success(
                        request,
                        "Great job! You fixed the content — your post is now automatically published!"
                    )
                else:
                    messages.success(request, "Post updated successfully.")

            updated_post.save()
            form.save_m2m()  # Important: save tags
            return redirect('post_detail', slug=updated_post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden("You cannot delete this post.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('post_list')

    return render(request, 'blog/post_delete.html', {'post': post})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            UserProfile.objects.create(user=user)
            UserPreference.objects.create(user=user)
            messages.success(request, "Account created successfully! Welcome!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_user(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile_settings(request):
    user = request.user
    profile = user.profile
    preference = user.preference

    avatar_form = AvatarUploadForm(instance=profile)
    profile_form = UserUpdateForm(instance=user)
    preference_form = UserPreferenceForm(instance=preference)

    if request.method == 'POST':
        if 'avatar_submit' in request.POST:
            avatar_form = AvatarUploadForm(request.POST, request.FILES, instance=profile)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, "Avatar updated successfully!")

        elif 'profile_submit' in request.POST:
            profile_form = UserUpdateForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile information updated successfully!")

        elif 'preferences_submit' in request.POST:
            preference_form = UserPreferenceForm(request.POST, instance=preference)
            if preference_form.is_valid():
                preference_form.save()
                messages.success(request, "Content preferences updated successfully!")

        return redirect('profile_settings')

    context = {
        'avatar_form': avatar_form,
        'profile_form': profile_form,
        'preference_form': preference_form,
    }
    return render(request, 'blog/profile_settings.html', context)


@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/user_posts.html', {'posts': posts})


def search_posts(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.filter(is_published=True)

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__in=[query])
        ).distinct()

    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})


@login_required
def ajax_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        posts = Post.objects.filter(is_published=True).filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__in=[query])
        ).distinct()[:10]
        results = [{'title': p.title, 'url': p.get_absolute_url()} for p in posts]
    return JsonResponse({'results': results})


# ——————— Helper: Cached Sentiment Score ———————
def get_post_sentiment_score_with_cache(post):
    """Get sentiment score with caching to avoid repeated expensive calls."""
    cache_key = f"post_sentiment_{post.id}"
    score = cache.get(cache_key)
    if score is None:
        full_text = f"{post.title} {post.content}"
        score = get_post_sentiment_score(full_text)
        cache.set(cache_key, score, timeout=60 * 60 * 24)  # Cache for 24 hours
    return score


# ——————— Enhanced Hybrid Recommendations: Fixed Related Name ———————
def get_recommendations(user, num_recommendations=4):
    """
    Smart Hybrid Recommendation System:
      - Base: Popularity (view count via postinteraction)
      - Boost: Matching user's preferred tags
      - Boost: Positive sentiment score
      - Exclude: Posts already viewed by user
    """
    if not user.is_authenticated:
        return list(
            Post.objects.filter(is_published=True)
            .annotate(view_count=Count('postinteraction', filter=Q(postinteraction__viewed=True)))
            .order_by('-view_count', '-created_at')[:num_recommendations]
        )

    # User's preferred tags
    try:
        preferred_tags = user.preference.preferred_tags.all()
        preferred_tag_names = {tag.name.lower() for tag in preferred_tags}
    except (UserPreference.DoesNotExist, AttributeError):
        preferred_tag_names = set()

    # Posts already viewed by user
    viewed_post_ids = PostInteraction.objects.filter(
        user=user, viewed=True
    ).values_list('post_id', flat=True)

    # Candidate posts
    candidates = Post.objects.filter(is_published=True).exclude(id__in=viewed_post_ids)

    scored_posts = []

    for post in candidates:
        # 1. Popularity score — use correct related_name: postinteraction
        view_count = post.postinteraction.filter(viewed=True).count()

        # 2. Tag matching boost
        post_tag_names = {tag.name.lower() for tag in post.tags.all()}
        tag_matches = len(post_tag_names.intersection(preferred_tag_names))
        tag_boost = tag_matches * 20

        # 3. Sentiment boost
        sentiment = get_post_sentiment_score_with_cache(post)
        sentiment_boost = (sentiment + 1.0) * 5  # Max +10

        # Final score
        total_score = view_count + tag_boost + sentiment_boost

        scored_posts.append((total_score, post))

    scored_posts.sort(key=lambda x: x[0], reverse=True)
    recommended_posts = [post for score, post in scored_posts[:num_recommendations]]

    # Fallback
    if len(recommended_posts) < num_recommendations:
        needed = num_recommendations - len(recommended_posts)
        fallbacks = candidates.exclude(id__in=[p.id for p in recommended_posts]) \
                              .annotate(view_count=Count('postinteraction', filter=Q(postinteraction__viewed=True))) \
                              .order_by('-view_count', '-created_at')[:needed]
        recommended_posts.extend(fallbacks)

    return recommended_posts