from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URL Examples:
# Web App: http://localhost:8000/
# Admin: http://localhost:8000/admin/
# API: http://localhost:8000/api/polls/

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Web App (HTML Pages)
    path('', include('polls.urls')),
    
    # API Endpoints
    path('api/', include('polls.api.urls')),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
