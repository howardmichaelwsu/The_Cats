from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('register', views.register),
	path('login', views.login),
	path('userhome', views.userhome),
	path('logout', views.logout),
	path('wallPost', views.wallPost),
	path('comment', views.comment),
	path('likes/<int:id>', views.likes),
]