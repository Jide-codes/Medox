from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path("", views.post_list, name='post_list'),
    path("add_post", views.new_post, name='new_post'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/',views.post_list_by_tag, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_details, name='post_detail'),
    path('<int:pk>/share/', views.post_share, name='post-share'),
    path('drafts/', views.my_draft, name='my_draft'),
    path('<int:pk>/', views.edit_draft, name='edit_draft'),
    path('author/<int:pk>/', views.authors, name='author_profile'),
    path('edit_profile/<int:pk>/', views.edit_profile, name='edit_profile'),


]
