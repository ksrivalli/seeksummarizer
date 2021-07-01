from os import name
from django.urls import path
from django.urls.conf import re_path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('short',views.short,name='short'),
    path('short_art',views.short_art,name='short_art'),
    path('short_text',views.short_text,name='short_text'),
    path('articles',views.articles,name='articles'),
    path('videos',views.videos,name='videos'),
    path('save_summary', views.save_summary, name='save_summary'),
    path('saved',views.saved,name='saved'),
    path('saved_title',views.saved_title,name='saved_title'),
    path('save_art',views.save_art,name='save_art'),
    path('get_sum',views.get_sum,name='get_sum'),
    path('get_vid_sum',views.get_vid_sum,name='get_vid_sum'),
    path('delete',views.delete,name='delete'),
    path('view_all_sum',views.view_all_sum,name='view_all_sum'),
    path('add_comment',views.add_comment,name='add_comment'),
    path('save_comment',views.save_comment,name='save_comment'),
    path('contact_form',views.contact_form,name='contact_form'),
    path('add_contact',views.add_contact,name='add_contact'),
    path('messages',views.messages,name='messages'),
]

