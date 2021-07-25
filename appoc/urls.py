from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('dashboard/', views.index, name="dashboard"),
	path('update_review/<str:pk>/', views.updateReview, name="update_review"),
	path('delete_review/<str:pk>/', views.deleteReview, name="delete_review"),
	path('create_review/', views.createReview, name="create_review"),
	path('request_review/', views.requestReview, name="request_review"),
]