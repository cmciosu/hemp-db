from django.contrib import admin
from django.urls import include, path

"""
Top-level URLs

- default: imports all routes in helloworld/urls.py
- admin/: django admin portal
- user/: django auth urls
"""
urlpatterns = [
    path("", include("helloworld.urls")),
    path('admin/', admin.site.urls),
    path("user/", include("django.contrib.auth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
