from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    save_on_top = True
    list_display = ('pk', 'title', 'author', 'created_at', 'views', 'category', 'get_photo')
    list_display_links = ('pk', 'title')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at', 'tags')
    readonly_fields = ('views', 'created_at', 'get_photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')

    get_photo.short_description = 'Photo'


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'pk')
    list_display_links = ('pk', 'title')
    search_fields = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'pk')
    list_display_links = ('pk', 'title')
    search_fields = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post', 'name', 'created_at')
    list_display_links = ('pk',)
    list_filter = ('post', 'created_at')
    search_fields = ('content',)


class EmailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'added_at')
    list_filter = ('added_at',)
    list_display_links = ('pk', 'email')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Email, EmailAdmin)
