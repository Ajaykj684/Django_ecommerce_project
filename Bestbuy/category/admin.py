from django.contrib import admin
from .models import Category,banner
# Register your models here.

admin.site.register(banner)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin),

