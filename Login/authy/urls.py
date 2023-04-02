from django.urls import path
from . import views

urlpatterns = [
	path('', views.Main, name='main'),
	path('user-signup/', views.Signup,name='user_signup'),
	path('user-login/', views.Login, name='user_login'),

]
