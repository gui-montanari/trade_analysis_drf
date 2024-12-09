from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),  # Certifique-se de ter o namespace
    path('users/', include('users.urls', namespace='users')),
    path('analysis/', include('analysis.urls', namespace='analysis')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)