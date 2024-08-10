from django.db import models
from django.http.request import uploadhandler
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField

class About(models.Model):
    name = models.CharField(_("name"), max_length=256)
    profile = models.CharField(_("profile") ,max_length=256)
    email = models.EmailField(_("email"), max_length=256)
    phone = models.CharField(_("phone"), max_length=100)
    description = models.TextField(_("description"))
    backgraund = ResizedImageField(crop=['middle', 'center'], upload_to='Profile/')
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='Profile/')
    content = RichTextField(_("content"))

    def __str__(self):
        return f"{self.name}"
    
class Category(models.Model):
    title = models.CharField(_("title"), max_length=256)

    class Meta:
        db_table = "category"
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return f"{self.title}"

class Portfile(models.Model):
    image = ResizedImageField(size=[400, 320], crop=['middle', 'center'], upload_to='Profile/')
    title = models.CharField(_("title"), max_length=256)
    date = models.DateField(_("date"), default=timezone.now)
    categories = models.ManyToManyField(Category, verbose_name=_("categories"), related_name="portfiles")
    
    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        db_table = "portfile"
        verbose_name = _("portfile")
        verbose_name_plural = _("portfiles")

class Profile(models.Model):
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='Profile/')
    title = models.CharField(_("title"), max_length=256)
    description = models.CharField(_("description"), max_length=256)
    
    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        db_table = "profile"
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

class BlogCategory(models.Model):
    title = models.CharField(_("title"), max_length=256)

    class Meta:
        db_table = "blog_category"
        verbose_name = _("blog category")
        verbose_name_plural = _("blog categories")

    def blog_count(self):
        return self.blogs.count()

    def __str__(self):
        return f"{self.title}"


class BlogTag(models.Model):
    title = models.CharField(_("title"), max_length=256)

    class Meta:
        db_table = "blog_tag"
        verbose_name = _("blog tag")
        verbose_name_plural = _("blog tags")

    def __str__(self):
        return f"{self.title}"
    
class Blog(models.Model):
    title = models.CharField(_("title"), max_length=256)
    slug = models.SlugField(_("slug"), max_length=256)
    categories = models.ManyToManyField(BlogCategory, related_name="blogs", verbose_name=_("categories"))
    is_top = models.BooleanField(_("blog is top"), default=False)
    description = models.TextField(_("description"))
    author = models.CharField(_("author"), max_length=256)
    tags = models.ManyToManyField(BlogTag, related_name="blogs", verbose_name=_("tags"))
    published_date = models.DateField(_("published date"), auto_now_add=True)
    main_image = ResizedImageField(_("main image"), size=[540, 304], crop=["middle", "center"], quality=95, upload_to="blog/")
    large_image = ResizedImageField(_("large image"), size=[1100, 700], crop=["middle", "center"], quality=95, upload_to="blog/")
    read_time = models.IntegerField(_("read time"))
    content = RichTextField(_("content"))

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "blog"
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")

    
class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments", verbose_name=_("blog"))
    name = models.CharField(_("name"), max_length=256)
    email = models.EmailField(_("email"), max_length=256)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, related_name="children", verbose_name=_("parent"))
    published_date = models.DateTimeField(_("published date"), auto_now_add=True)
    comment = models.TextField(_("comment"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "blog_comment"
        verbose_name = _("blog comment")
        verbose_name_plural = _("blog comments")


class Contact(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=64)
    subject = models.CharField(max_length=256)
    message = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "contact"
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")
