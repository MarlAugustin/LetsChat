from django.shortcuts import render,redirect
from .forms import SignUpForm, UpdateUserForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from friends.models import Friendlist, FriendRequest
from django.contrib.auth.models import User
from django.http import HttpResponse
from friends.utils import get_friend_request_or_false
from friends.friend_request_status import FriendRequestStatus
# Create your views here.
"""
This is the profile view where the user can update their profile
If the forms are valid, the user informations are updated and a success message is displayed
Else the form errors are displayed
"""
@login_required(login_url='/login/')
def profile(request):
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been successfuly updated!')
            return redirect('profile')
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        try:
            #This accesses the other user account friends list, if the user doesn't have a friend list, we create one.
            friend_list = Friendlist.objects.get(user=request.user)
        except Friendlist.DoesNotExist:
            friend_list = Friendlist(user=request.user)
            friend_list.save()
        friends = friend_list.friends.all()
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'friends' : friends
    }
    return render(request,'users/profile.html', context)
"""
Other_profile is called when the authenticated user tries to see a profile which is different from his own
"""
@login_required(login_url='/login/')
def other_profile(request, username):
    context = {}
    try:
        account = User.objects.get(username=username)
    except:
        return HttpResponse("Something went wrong")
    context['account'] = account
    user = request.user
    if account != user:
        #If the username that was searched was different than the connected user
        try:
            #This accesses the other user account friends list, if the user doesn't have a friend list, we create one.
            friend_list = Friendlist.objects.get(user=account)
        except Friendlist.DoesNotExist:
            friend_list = Friendlist(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends
        request_sent = None
        request_id = None 
        if user in friends:
            context['is_friend'] = True
        else:
            context['is_friend'] = False
            #case 1 : Request sent by this user to you
            if get_friend_request_or_false(sender=account, receiver=user) != False:
                request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                context['pending_friend_request_id'] = get_friend_request_or_false(
                    sender=account, receiver=user
                ).id
            #case 2: Request sent by you to this user
            elif get_friend_request_or_false(sender=user, receiver=account) != False:
                request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
            else:
                request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        context['request_sent'] = request_sent
        return render(request, 'users/other_profiles.html', context)
    else:
        #if the user that is connected and the username are the same
        return redirect('profile')
"""
THis is the registration view where the user can register for an account
if the form is valid, the user is saved and is logged in
else the form errors are displayed
"""
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, your account has been successfuly created. You are now part of our community')
            #Adding the creation of a friend list 
            account = User.objects.get(username=username)
            friend_list = Friendlist(user=account)
            friend_list.save()
            return redirect('login')
        else: 
            messages.warning(request,form.errors)

    else: 
        form = SignUpForm()
    return render(request, 'users/register.html',{'form':form})

@login_required(login_url='/login/')
def users(request):
    context = {}
    username = '' 
    user = request.user
    if request.GET:
            username = request.GET.get('username','')
            context['username'] = username
    if username == '' :
        users = User.objects.all()
    else :
        users =  User.objects.filter(username__contains=username).exclude(username__contains=user.username)
    #This accesses the other user account friends list, if the user doesn't have a friend list, we create one.
    try:
        friend_list = Friendlist.objects.get(user=user)
    except Friendlist.DoesNotExist:
        friend_list = Friendlist(user=user)
        friend_list.save()
    friends = friend_list.friends.all()
    context['friends'] = friends
    context['users'] = users 
    return render(request, 'users/users_list.html', context)
    