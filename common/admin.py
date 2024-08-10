from django.contrib import admin

from common import models


admin.site.register(models.BlogCategory)
admin.site.register(models.BlogTag)
admin.site.register(models.BlogComment)
admin.site.register(models.Profile)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", )

@admin.register(models.Portfile)
class PortfileAdmin(admin.ModelAdmin):
    list_display = ("title", )

@admin.register(models.About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("name", )

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", ) 
    prepopulated_fields = {"slug": ("title",)}

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject")
    list_filter = ("email", )
    search_fields = ("name", "email", "subject", "message")