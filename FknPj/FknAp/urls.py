from django.urls import path
from . import views

app_name = 'FknAp'

urlpatterns = [
    
    path("createpost", views.create_post, name="create_post"),
    path("n/post/<int:post_id>/edit", views.edit_post, name="edit_post"),
    path("n/post/<int:post_id>/delete", views.delete_post, name="delete_post"),
    path("n/post/<int:post_id>/comments", views.comments, name="comments"),
    path('comment/<int:post_id>/<int:comment_id>/add_reply/', views.add_reply, name='add_reply'),
    path('comment/<int:post_id>/<int:comment_id>/delete/', views.delete_comment, name='comment_delete'),

]
