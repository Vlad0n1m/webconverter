from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', LogoutView.as_view(),  name='logout'),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
