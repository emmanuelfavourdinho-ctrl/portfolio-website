from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("work/<slug:slug>/", views.case_study, name="case_study"),
    path("robots.txt", views.robots),
    path("sitemap.xml", views.sitemap),
    path("admin/", admin.site.urls),
]
