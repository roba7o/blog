# Django Blog Application

This is a full-featured blog web application built using **Django**, with multiple functionalities that showcase my skills in web development, database management, and advanced search features. The project includes post management, commenting, tagging, search, and an admin panel for managing the blog content.

## Key Features

### Blog Website

- **Post Management**: Users can view blog posts, which are paginated and displayed with custom tags. Each post has its own detail view, comment section, and similar posts recommendations.
- **Tagging System**: Implemented with `django-taggit` to allow easy tagging of posts. Users can also filter posts by tags.
- **Markdown Support**: Posts can be written in Markdown, providing rich text formatting options.
- **Post Sharing**: Users can share blog posts via email with a custom message.
- **Comments**: Each post has a comment section where users can add their thoughts.

### Search

- **Advanced Search Functionality**: The search view supports stemming, ranking, weighted queries, and trigram similarity for more accurate and relevant search results.
- **Custom Search Ranking**: Search results are ranked based on relevance, using a combination of stemming and trigram similarity for intelligent searching.

### Sitemap & RSS Feed

- **Sitemap**: Auto-generated sitemap for SEO optimization, including all blog posts and tags using `django-taggit`.
- **RSS Feed**: RSS feed is available for the latest posts to keep readers updated on new content.

### Pagination & Popular Posts

- **Pagination**: Blog posts are displayed with pagination, allowing users to browse through content seamlessly.
- **Most Commented and Latest Posts**: Sidebar widgets display the most commented and most recent posts.

### SEO & Similar Posts

- **Canonical URLs**: Ensures each post has a canonical URL for better SEO.
- **Similar Posts**: Related posts are suggested at the end of each blog post, based on similar tags.

## URLs & Views

The following URL patterns are defined to manage the blog's different views:

python

Copy code

`urlpatterns = [     path('', views.post_list, name='post_list'),     path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),     path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),     path('<int:post_id>/share/', views.post_share, name='post_share'),     path('<int:post_id>/comment/', views.post_comment, name='post_comment'),     path('feed/', LatestPostsFeed(), name='post_feed'),     path('search/', views.post_search, name='post_search'), ]`

## Admin Panel

- The Django **admin interface** allows for easy management of posts, comments, and tags.

## Database

- **PostgreSQL (Docker)**: The application uses a PostgreSQL database, which was set up using a **data dump/load** from a SQLite test environment.
- **Data Migration**: Migration from SQLite to PostgreSQL was achieved by exporting the data from the SQLite test environment and importing it into a Dockerized PostgreSQL instance.

## Technology Stack

- **Backend**: Django 5.0.4
- **Database**: PostgreSQL (via Docker) with initial data dump/load from SQLite
- **Frontend**: Bootstrap for responsive design
- **Search Engine**: Advanced search using Django’s query capabilities with stemming, trigram similarity, and ranking
- **Additional Features**: RSS Feed, Sitemap, Markdown support, `django-taggit` for tagging

## Templates & Views

- **Base Template**: Includes reusable components for consistent styling across pages.
- **Custom Template Tags**: For custom functionality in templates.
- **Class-Based Views**: Used in certain sections of the application for better code structure and reuse.
- **Model Forms**: For creating and updating posts, comments, and tags.

## How to Run

1. Clone the repository:
    
    bash
    
    Copy code
    
    `git clone https://github.com/yourusername/blog-app.git`
    
2. Set up the virtual environment and install dependencies:
    
    bash
    
    Copy code
    
    `python3 -m venv venv source venv/bin/activate pip install -r requirements.txt`
    
3. Run PostgreSQL via Docker:
    
    bash
    
    Copy code
    
    `docker-compose up -d`
    
4. Migrate the database:
    
    bash
    
    Copy code
    
    `python manage.py migrate`
    
5. Run the development server:
    
    bash
    
    Copy code
    
    `python manage.py runserver`
    

## Future Enhancements

- **User Authentication**: Plan to integrate user registration and login for a more personalized experience.
- **Improved Comment Moderation**: Admin features for moderating comments.
- **Enhanced SEO Features**: Implementing more meta tags and structured data for SEO optimization.