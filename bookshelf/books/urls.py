from django.urls import include, path

from . import views

urlpatterns = [
    # Admin permissions required
    path('', views.BookListAPIView.as_view()),
    path('<int:id>/', views.BookUpdateDeleteAPIView.as_view()),
    path('<int:id>/detail', views.BookDetailAPIView.as_view()),
    path('add/', views.BookCreateAPIView.as_view()),
    
    # Common user actions
    path('my/', views.BookUserListAPIView.as_view()),
    path('my/<int:id>/', views.BookUserAPIView.as_view()),
]