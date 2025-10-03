from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.landing_page,name='landing_page'),
    path('signup',views.signup_page,name='signup'),
    path('login',views.login_page, name='login'),
    path('create_account', views.create_account, name='create_account'),
    path('signin', views.signin, name='signin'),
    path('home', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('add_experience', views.add_experience, name='add_experience'),
    path('add_education', views.add_education, name='add_education'),
    path('education/<int:id>/json/', views.education_detail, name='education_detail'),
    path("experience/<int:id>/json/", views.experience_detail, name="experience_detail"),
    path("userprofile/<int:id>/json/", views.userprofile_detail, name="userprofile_detail"),
    path("update_profile/<int:id>/", views.update_profile, name="update_profile"),
    path('update_profile_photo/', views.update_profile_photo, name='update_profile_photo'),
    path('update_cover_photo/', views.update_cover_photo, name='update_cover_photo'),
    path('update_experience/<int:id>/', views.update_experience, name='update_experience'),
    path('update_education/<int:id>/', views.update_education, name='update_education'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('view_profile/<int:id>/', views.view_profile, name='view_profile'),
    path('add_comment',views.add_comment,name='add_comment'),
    path('user_activity',views.user_activity,name='user_activity'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),
]