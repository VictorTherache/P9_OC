from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
	path('abonnements', views.abonnements, name="abonnements"),
	path('update_review/<str:pk>/', views.updateReview, name="update_review"),
	path('delete_review/<str:pk>/', views.deleteReview, name="delete_review"),
	path('update_ticket/<str:pk>/', views.updateTicket, name="update_ticket"),
	path('delete_ticket/<str:pk>/', views.deleteTicket, name="delete_ticket"),
	path('unfollow/<str:pk>/', views.unfollow, name="unfollow"),
	path('follow_user/<str:pk>/', views.follow, name="follow_user"),
	path('create_review/', views.createReview, name="create_review"),
	path('create_ticket/', views.createTicket, name="create_ticket"),
	path('answer_ticket/<str:pk>/', views.answerTicket, name="answer_ticket"),
] 