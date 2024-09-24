from django.contrib.sitemaps import _SupportsCount, _SupportsLen, _SupportsOrdered, Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9          #indicating that blog posts are VERY important

    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated
    
