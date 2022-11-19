from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('category/<str:slug>/', GetCategory.as_view(), name='category'),
    path('post/<str:slug>/', ShowPost.as_view(), name='post'),
    path('tag/<str:slug>/', ShowPostByTag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
    path('comment_form/<str:slug>/', AddComment.as_view(), name='comment_form'),
    path('contact_form/', Contact.as_view(), name='contact_form')
]
