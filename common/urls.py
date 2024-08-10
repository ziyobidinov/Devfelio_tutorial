from django.urls import path

from common import views

app_name = "common"


urlpatterns = [
        path("", views.HomeView.as_view(), name="home"),
        path("blogs/", views.BlogListView.as_view(), name="blog"),
        path("blogs/<str:slug>/", views.BlogDetailView.as_view(), name="blog-single"),
        path("add_comment/<int:blog_id>/", views.AddComment.as_view(), name="blog-comment"),
        path("contact/", views.ContactView.as_view(), name="contact"),
        ]