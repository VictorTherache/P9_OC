from appoc.follow_user import FollowUser
from appoc.create_ticket import TicketForm
from appoc.create_review import ReviewForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from .models import Ticket, Review, UserFollows
from .forms import CreateUserForm


def dashboard(request):
    all_posts = []
    my_posts = []
    my_follows = []
    reviews = Review.objects.all()
    tickets = Ticket.objects.all()
    for review in reviews:
        all_posts.append(review)
    for ticket in tickets:
        all_posts.append(ticket)
    relationships = UserFollows.objects.all()
    for relation in relationships:
        if relation.user == request.user:
            my_follows.append(relation.followed_user)
    for post in all_posts:
        for follow in my_follows:
            if follow == post.user or post.user == request.user:
                my_posts.append(post)
    my_posts.sort(key=lambda r: r.time_created)
    my_posts = my_posts[::-1]
    my_posts = list(dict.fromkeys(my_posts))
    print(my_posts)
    context = {'my_posts': my_posts}
    return render(request, 'accounts/dashboard.html', context)


def deleteReview(request, pk):
    item = Review.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/dashboard')

    context = {'item': item}
    return render(request, 'accounts/delete_review.html', context)


def deleteTicket(request, pk):
    item = Ticket.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/dashboard')

    context = {'item': item}
    return render(request, 'accounts/delete_ticket.html', context)


def updateReview(request, pk):
    review = Review.objects.get(id=pk)
    form = ReviewForm(instance=review)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context = {'form': form}
    return render(request, 'accounts/update_review.html', context)


def updateTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    form = TicketForm(instance=ticket)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context = {'form': form}
    return render(request, 'accounts/update_ticket.html', context)


def answerTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    review_form = ReviewForm(request.POST or None)
    context = {'ticket': ticket, 'review_form': review_form}
    if request.method == 'POST':
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review_form.save()
            return redirect('/dashboard')
    return render(request, 'accounts/answer_ticket.html', context)


def createReview(request):
    review_form = ReviewForm(request.POST or None)
    form = TicketForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            ticket_form = form.save(commit=False)
            ticket_form.user = request.user
            ticket_form.save()
    if request.method == 'POST':
        if review_form.is_valid():
            ticket = Ticket.objects.all().last()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('/dashboard')
        else:
            form = ReviewForm(request.POST)
    context = {'form': form, 'review_form': review_form}
    return render(request, 'accounts/create_review.html', context)


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
    current_user = ''
    users = User.objects.values()
    relation = FollowUser(request.POST or None)
    if request.method == 'POST':
        for user in users:
            if pk == user['username']:
                pk = User.objects.get(username=user['username'])
            if str(request.user) == user['username']:
                current_user = User.objects.get(username=user['username'])
        relation = FollowUser(request.POST)
        relation.user = current_user
        relation.followed_user = pk
        relation_object = relation.save(commit=False)
        relation_object.user = request.user
        relation_object.followed_user = pk
        relation.save()
        return redirect('abonnements')
    else:
        relation = FollowUser()
    context = {'relation': relation, 'pk': pk}
    return render(request, 'accounts/follow_user.html', context)


def unfollow(request, pk):
    current_user = User.objects.get(username=str(request.user))
    followed = User.objects.get(id=pk)
    relationship = UserFollows.objects.get(user=current_user,
                                           followed_user=followed)
    print(relationship)
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
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
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
    context = {}
    return render(request, 'accounts/dashboard.html', context)


def abonnements(request):
    current_user = request.user
    all_relationship = UserFollows.objects.all()
    users = User.objects.values()
    searched_users = []
    my_follows = []
    my_follows_str = []
    for follower in all_relationship:
        if follower.user == request.user:
            my_follows.append(follower.followed_user)
            my_follows_str.append(str(follower.followed_user))
    if request.method == 'POST':
        context = {'all_relationship': all_relationship,
                   'my_follows_str': my_follows_str,
                   'my_follows': my_follows,
                   'searched_users': searched_users,
                   'current_user': current_user,
                   }
        name = request.POST['search_user']
        for user in users:
            if name in user['username']:
                searched_users.append(str(user['username']))
    context = {'all_relationship': all_relationship,
               'my_follows_str': my_follows_str,
               'my_follows': my_follows,
               'searched_users': searched_users,
               'current_user': current_user,
               }
    return render(request, 'accounts/abonnements.html', context)
