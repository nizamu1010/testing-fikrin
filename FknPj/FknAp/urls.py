from django.urls import path
from . import views

app_name = 'FknAp'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('terms/', views.terms_and_conditions, name='terms'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('profile_cropping/<int:user_id>/', views.profile_cropping, name="profile_cropping"),
    path("createpost", views.create_post, name="create_post"),
    path("n/post/<int:post_id>/edit", views.edit_post, name="edit_post"),
    path("n/post/<int:post_id>/delete", views.delete_post, name="delete_post"),
    path("n/post/<int:post_id>/comments", views.comments, name="comments"),
    path('comment/<int:post_id>/<int:comment_id>/add_reply/', views.add_reply, name='add_reply'),
    path('comment/<int:post_id>/<int:comment_id>/delete/', views.delete_comment, name='comment_delete'),
]
