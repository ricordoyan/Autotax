from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tax_processing.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', auth_views.obtain_auth_token),  # Token authentication endpoint
    # Serve React app - this should be the last URL pattern
    re_path('.*', TemplateView.as_view(template_name='index.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add CORS headers to responses
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

def cors_response(get_response):
    def middleware(request):
        if request.method == "OPTIONS":
            response = HttpResponse()
        else:
            response = get_response(request)
        
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
    return middleware 