from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.UserViewSet.as_view(), name='get_user_url'),
    path('all/', views.UserListView.as_view(), name='users_list_url'),
    
    path('reg/', views.CustomRegistrationView.as_view({"post": "create"}), name='users_ref_url'),
    path('profile/', views.ProfileViewSet.as_view(), name='users_profile_url'),
]