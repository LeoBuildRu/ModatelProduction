from django.contrib import admin

# Register your models here.
from .models import *

class SizeTublerInline(admin.TabularInline):
    model = Sizes

class ImagesTublerInline(admin.TabularInline):
    model = Images

class TagTublerInline(admin.TabularInline):
    model = Tag

class StuffTublerInline(admin.TabularInline):
    model = Stuff

class ProductAdmin(admin.ModelAdmin):
    inlines = [StuffTublerInline, SizeTublerInline, ImagesTublerInline, TagTublerInline]

class PostTublerInline(admin.TabularInline):
    model = WebPostCategories

class PostsAdmin(admin.ModelAdmin):
    inlines = [PostTublerInline]

admin.site.register(Categories)
admin.site.register(Color)
admin.site.register(MaterialType)
admin.site.register(SizeCatalog)
admin.site.register(Product, ProductAdmin)
admin.site.register(WebPostType)
admin.site.register(WebThemePost)
admin.site.register(WebSubThemePost)
admin.site.register(WebPost, PostsAdmin)

