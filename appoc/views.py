from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import CreateUserForm
from .create_review import *

def index(request):
	reviews = Review.objects.all()
	form = ReviewForm()
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/dashboard')
	context = {'reviews':reviews, 'form':form}
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

def createReview(request):
	form = ReviewForm()
	context = {'form': form}
	return render(request, 'accounts/create_review.html', context)

def requestReview(request):
	form = ReviewForm()
	context = {'form': form}
	return render(request, 'accounts/request_review.html', context)

def deleteReview(request, pk):
	item = Review.objects.get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('/dashboard')

	context = {'item':item}
	return render(request, 'accounts/delete_review.html', context)

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