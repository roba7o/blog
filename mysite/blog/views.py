from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

from .models import Post
from taggit.models import Tag
from django.db.models import Count
from .forms import EmailPostForm, CommentForm, SearchForm


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url
            )
            print(f"post url is {post_url}")
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None, #Therefore will use the DEFAULT_FROM_EMAIL setting
                recipient_list=[cd['to']]
            )
        sent = True
    else:
        form = EmailPostForm()
    
    return render(
        request, 
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )
    

class PostListView(ListView):
    """
    Alternative Post List View
    """

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    #pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        #if the page number does not exist, get the last page of results
        #total number of pages is the last page... 
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {
            'posts': posts,
            'tag': tag
        }
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)  #returns a list of tag ids for current post

    similar_posts = Post.published.filter(  # returns a list of posts with ids existing in the above list 
        tags__in=post_tags_ids
    ).exclude(id=post.id)

    similar_posts = similar_posts.annotate(     # adds a same_tags attribute to each post
        same_tags=Count('tags')                 # annotate() is chained to filter() above
    ).order_by('-same_tags', '-publish')[:4]


    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            "comments":comments,
            "form": form,
            "similar_posts": similar_posts
        }
    )

@require_POST   # Only allow POST requests for this view
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment=None # if the form is invalid, the if statement is skipped and the empty comment object still rendered.

    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Creating a comment object but not yet storing it in database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # NOW... saving the comment to the database
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post':post,
            'form':form,
            'comment':comment
        }
    )


def post_search(request):
    form = SearchForm
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = (
                Post.published.annotate(
                    # search=search_vector,
                    # rank=SearchRank(search_vector, search_query)
                    similarity = TrigramSimilarity('title', query)
                )
                # .filter(rank__gte=0.3)
                # .order_by('-rank')
                .filter(similarity__gt=0.1)
                .order_by('-similarity')
            )
    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )

