from django.urls import path
from . import views

urlpatterns = [
    path('search_results',views.search_results,name='search_results'),
    path("send_request/<int:id>/", views.create_connection_request, name="create_connection_request"),
    path('delete_request/<int:receiver_id>/', views.delete_connection_request, name='delete_connection_request'),
    path('accept-request/',views.accept_connection_request,name='accept_connection_request'),
    path('create_post/', views.create_post, name='create_post'),
    path('delete_connection/<int:user_id>/', views.delete_connection, name='delete_connection'),
    path("toggle-like-post/", views.toggle_like_post, name="toggle-like-post"),
    path("comment-page", views.comment_page, name="comment_page"),
    path("my_connections", views.my_connections, name="my_connections"),
    path("edit_post/<int:id>/", views.edit_post, name="edit_post"),
]