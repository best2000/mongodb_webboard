"""webBoard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home , name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('create_topic', views.create_topic, name = 'create_topic'),
    path('create_comment/<str:topic_id>', views.create_comment, name = 'create_comment'),

    path('topic/<str:topic_id>', views.view_topic, name = 'view_topic'),

    path('edit_topic/<str:topic_id>', views.edit_topic, name = 'edit_topic'),
    path('edit_comment/<str:comment_id>', views.edit_comment, name = 'edit_comment'),

    path('delete_topic/<str:topic_id>', views.delete_topic, name = 'delete_topic'),
    path('delete_comment/<str:comment_id>', views.delete_comment, name = 'delete_comment'),

    path('like_topic/<str:topic_id>', views.like_topic, name = 'like_topic'),
    path('unlike_topic/<str:topic_id>', views.unlike_topic, name = 'unlike_topic'),

    path('like_comment/<str:comment_id>', views.like_comment, name = 'like_comment'),
    path('unlike_comment/<str:comment_id>', views.unlike_comment, name = 'unlike_comment'),

    path('tags/<str:tag>', views.show_tag, name = 'show_tag'),
]
