from appoc.follow_user import FollowUser
from appoc.create_ticket import TicketForm
from appoc.create_review import ReviewForm

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
from .models import *
from .forms import CreateUserForm
from .create_review import *

def dashboard(request):
	reviews = Review.objects.all()
	tickets = Ticket.objects.all()
	for ticket in tickets:
		print(ticket.reviews)
			# print(ticket.title)
			# if review.ticket.id == ticket.id: 
			# 	if (ticket.user == str(request.user.get_username())):
			# 		css_value = 'hidden'
			# 	else:
			# 		css_value = ''
	# for ticket in tickets:
	# # 	if(ticket.image):
	# 	print(ticket.image.url)
	# form = ReviewForm()
	# if request.method == 'POST':
	# 	form = ReviewForm(request.POST)
	# 	if form.is_valid():
	# 		form.save()
	# 	return redirect('/dashboard')
	context = {'reviews':reviews, 'tickets':tickets}
	return render(request, 'accounts/dashboard.html', context)

def updateReview(request, pk):
	review = Review.objects.get(id=pk)
	form = ReviewForm(instance=review)
	if request.method == 'POST':
		form = ReviewForm(request.POST, instance=review)
		if form.is_valid():
			form.save()
			return redirect('/dashboard')
	context = {'form':form}
	return render(request, 'accounts/update_review.html', context)

def answerTicket(request, pk):
	ticket = get_object_or_404(Ticket, pk=pk)
	ticket = Ticket.objects.get(id=pk)
	review_form = ReviewForm(request.POST or None)
	context = {'ticket':ticket, 'review_form':review_form}
	if request.method == 'POST':
		if review_form.is_valid():
			review = review_form.save(commit=False)
			review.ticket = ticket
			review.user = request.user
			review_form.save()
			return redirect('/dashboard')
	return render(request, 'accounts/answer_ticket.html', context)

def createReview(request):
	print(request)
	form = TicketForm(request.POST or None)
	review_form = ReviewForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			ticket_form = form.save(commit=False)
			ticket_form.user = request.user
			ticket_form.save()
	if request.method == 'POST':
		print(review_form)	
		if review_form.is_valid():
			ticket = Ticket.objects.all().last()
			review = review_form.save(commit=False)
			review.user = request.user
			review.ticket = ticket
			review.save()
			return redirect('/dashboard/')
		else:
			form = ReviewForm(request.POST)
	context = {'form': form, 'review_form': review_form}
	return render(request, 'accounts/create_review.html', context)
	# if request.method == 'POST':
	# 	ticket_form = TicketForm(request.POST)
	# 	review_form = ReviewForm(request.POST)
	# 	if ticket_form.is_valid() and review_form.is_valid():
	# 		ticket_form.save()
	# 		review_form.save()
	# 		return redirect('/dashboard')        

	# 	else:
	# 		context = {
	# 			'ticket_form': ticket_form,
	# 			'review_form': review_form,
	# 		}

	# else:
	# 	context = {
	# 		'ticket_form': TicketForm(),
	# 		'review_form': ReviewForm(),
	# 	}
	# return render(request, 'accounts/create_review.html', context)


def createTicket(request):
	form = TicketForm()
	if request.method == 'POST':
		form = TicketForm(request.POST, request.FILES)
		if form.is_valid():
			form_object = form.save(commit=False)
			form_object.user = request.user
			form_object.save()
			return redirect('/dashboard')
		else:
			form = TicketForm(user=request.user)
	context = {'form': form}
	return render(request, 'accounts/create_ticket.html', context)

def follow(request, pk):
	print(pk)
	relation = FollowUser()
	if request.method == 'POST':
		relation = FollowUser(request.POST)
		if relation.is_valid():
			relation_object = relation.save(commit=False)
			relation_object.user = request.user
			relation_object.save()
			return redirect('abonnements')
		else:
			relation = FollowUser(user = request.user)
	context = {'relation': relation, 'pk': pk}
	return render(request, 'accounts/follow.html', context)

def deleteReview(request, pk):
	item = Review.objects.get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('/dashboard')

	context = {'item':item}
	return render(request, 'accounts/delete_review.html', context)

def unfollow(request, pk):
	relationship = UserFollows.objects.get(id=pk)

	if request.method == 'POST':
		relationship.delete()
		return redirect('abonnements')
	context = {'relationship': relationship}
	return render(request, 'accounts/unfollow.html', context)




def registerPage(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('dashboard')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def home(request):
	# orders = Order.objects.all()
	# customers = Customer.objects.all()

	# total_customers = customers.count()

	# total_orders = orders.count()
	# delivered = orders.filter(status='Delivered').count()
	# pending = orders.filter(status='Pending').count()

	# context = {'orders':orders, 'customers':customers,
	# 'total_orders':total_orders,'delivered':delivered,
	# 'pending':pending }
    context = {}
    return render(request, 'accounts/dashboard.html', context)

def abonnements(request):
	current_user = request.user
	all_relationship = UserFollows.objects.all()
	users = User.objects.values()
	searched_users = []
	my_follows = []
	my_follows_str = []

	is_he_following_me = []
	for follower in all_relationship:
		if follower.user == request.user:
			my_follows.append(follower.followed_user)
			my_follows_str.append(str(follower.followed_user))
	if request.method == 'POST':
		context = {'all_relationship': all_relationship, 
			'my_follows_str':my_follows_str, 
			'my_follows': my_follows,
			'searched_users':searched_users, 
			'current_user':current_user,
			'is_he_following_me':is_he_following_me,}
		name = request.POST['search_user']
		for user in users:
			if name in user['username']:
				searched_users.append(str(user['username']))
		for user in searched_users:
			for follow in users:
				if str(follow['username']) == str(user):
					is_he_following_me.append([str(follow['username']), 1])
				else:
					is_he_following_me.append([str(follow['username']), 0])
	print(type(my_follows[0]))
	# if 'domi' in my_follows.values():
	# 	print('VALIDE')
	context = {'all_relationship': all_relationship, 
				'my_follows_str':my_follows_str, 
				'my_follows': my_follows,
				'searched_users':searched_users, 
				'current_user':current_user,
				'is_he_following_me':is_he_following_me,}
	return render(request, 'accounts/abonnements.html', context)

# {% if relation.followed_user|stringformat:"i" == user|stringformat:"i" %}
