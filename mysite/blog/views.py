from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post
from .forms import EmailPostForm

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.status.PUBLISHED
    )

    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            # ...send email

    else:
        form = EmailPostForm()
    
    return render(
        request, 
        'blog/post/share.html',
        {
            'post': post,
            'form': form
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


def post_list(request):
    post_list = Post.published.all()
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
        {'posts': posts}
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
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )

