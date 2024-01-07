from django.urls import path
from . import views

app_name = 'Authentication'

urlpatterns = [

    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('terms/', views.terms_and_conditions, name='terms'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('profile_cropping/<int:user_id>/', views.profile_cropping, name="profile_cropping"),

    path('save-token/', views.save_token, name='save_token'),
]


