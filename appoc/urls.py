from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
	path('update_review/<str:pk>/', views.updateReview, name="update_review"),
	path('delete_review/<str:pk>/', views.deleteReview, name="delete_review"),
	path('create_review/', views.createReview, name="create_review"),
	path('create_ticket/', views.createTicket, name="create_ticket"),
	path('answer_ticket/<str:pk>/', views.answerTicket, name="answer_ticket"),

]