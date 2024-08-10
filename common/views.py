from django.views import View
from django.views.generic import DetailView, ListView
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


from common import models
from common.forms import BlogCommentForm 


class HomeView(View):
    def get(self, request):
        abouts = models.About.objects.all()
        portfiles = models.Portfile.objects.all().prefetch_related("categories")
        category = models.Category.objects.all()
        testimonials = models.Profile.objects.all()
        blog = models.Blog.objects.filter(is_top=True).prefetch_related("categories").order_by("-id")[:3]

        
        context = {
            "abouts": abouts,
            "portfiles": portfiles,
            "category": category,
            "testimonials": testimonials,
            "blogs": blog,
        }
        return render(request, 'index.html', context)

class BlogListView(ListView):
    model = models.Blog
    template_name = "blog.html"
    context_object_name = "objects"
    paginate_by = 3


class BlogDetailView(DetailView):
    queryset = models.Blog.objects.all().prefetch_related("categories")
    slug_field = "slug"
    context_object_name = "object"
    template_name = "blog-single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["related_blogs"] = models.Blog.objects.filter(
                ~Q(slug=self.kwargs["slug"]), categories__in=self.get_object().categories.all()
                ).prefetch_related("categories").distinct()[:4]
        context["categories"] = models.BlogCategory.objects.all().prefetch_related("categories").annotate(count=Count("blogs"))
        context["comments"] = models.BlogComment.objects.filter(blog__slug = self.kwargs["slug"])

        return context

class AddComment(View):
    def post(self, request, blog_id):
        if request.method == 'POST':
            form = BlogCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                blog = get_object_or_404(models.Blog, id=blog_id)
                comment.blog = blog
                form.save()
                return HttpResponseRedirect(reverse("common:blog-single", kwargs= {"slug": blog.slug}))

        else:
            form = BlogCommentForm()

        return render(request, 'blog-single.html', {'form': form})
    
class ContactView(View): 
    def get(self, request):
        return render(request,"contact-us.html")
    
    def post(self, request):   
        name = request.POST.get("name")
        subject = request.POST.get("subject")
        email = request.POST.get("email")
        message = request.POST.get("message")

        try:
            models.Contact.objects.create(name = name, email = email, subject = subject, message = message)
            messages.add_message(request, messages.SUCCESS, "Your Massage has been sent successfully!")
            return HttpResponseRedirect(reverse("common:contact"))
        
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'Error occurred! Please try again! ')
            return HttpResponseRedirect(reverse("common:contact"))

