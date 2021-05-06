from django.urls import path
from basic_app import views

urlpatterns = [
    path('about/',views.AboutView.as_view(),name='about'),
    path('',views.PostListView.as_view(),name='post_list'),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
    path('post/create/',views.PostCreateView.as_view(),name='post_create'),
    path('post/update/<int:pk>',views.PostUpdateView.as_view(),name='post_update'),
    path('post/delete/<int:pk>',views.PostDeleteView.as_view(),name='post_delete'),
    path('draft/',views.DraftListView.as_view(),name='draft_list'),
]
