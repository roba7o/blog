from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post
from taggit.models import Tag

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9          #indicating that blog posts are VERY important

    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated
    
class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        # Return all tags used in the posts
        return Tag.objects.all()
    
    def location(self, obj):
        # Generate URL for each tag
        return reverse('blog:post_list_by_tag', args=[obj.slug])
    
    
