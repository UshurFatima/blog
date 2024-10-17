from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListCreateAPIView.as_view()),
    path('<int:id>/', views.post_detail_api_view),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('search_words/', views.SearchWordViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('search_words/<int:id>/', views.SearchWordViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    }))
]
