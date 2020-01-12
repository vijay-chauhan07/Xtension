from django.contrib import admin
from .models import Post, Profile, Comment
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'dob','country', 'city','website','mobile', 'photo')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ['title','author__username']
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')
    ordering =['title']
    actions = ['make_published']
    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description ="mark selected stories as published"




 

admin.site.register(Comment)  

admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)



