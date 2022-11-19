from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View
from django.db.models import F

from blog.forms import CommentForm, ContactForm
from blog.models import *


# Create your views here.
class HomePage(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        random_post = Post.objects.order_by("?").first()
        context['random_post'] = random_post
        context['title'] = 'Home page'
        return context


# def home_page(request):
#     posts = Post.objects.all()
#     random_post = Post.objects.order_by("?").first()
#     context = {
#         'posts': posts,
#         'random_post': random_post
#     }
#     return render(request, 'blog/index.html', context=context)


class GetCategory(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


# def get_category(request, slug):
#     post = Post.objects.filter(category__slug=slug)
#     return render(request, 'blog/category.html', {'posts': post})
#

class ShowPost(DetailView):
    model = Post
    # slug_url_kwarg = 'slug'
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['comments'] = Comment.objects.filter(post__slug=self.kwargs['slug'])
        return context


# def get_post(request, slug):
#     return render(request, 'blog/single.html')


class ShowPostByTag(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


# class AddComment(CreateView):
#     form_class = CommentForm
#     template_name = 'blog/form.html'
#     success_url = reverse_lazy('home')

class AddComment(View):
    def post(self, request, slug):
        form = CommentForm(request.POST)
        print(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = Post.objects.get(slug=slug)
            obj.save()
        else:
            print(form.errors)
        return redirect('post', slug)


class Contact(CreateView):
    form_class = ContactForm
    model = Email
    success_url = reverse_lazy('home')
