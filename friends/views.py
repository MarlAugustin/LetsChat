from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Friendlist, FriendRequest
from .utils import get_friend_request_or_false
from .friend_request_status import FriendRequestStatus
from django.contrib import messages
import json
# Create your views here.
@login_required(login_url='/login/')
def friend_requests_view(request):
    user = request.user
    context = {}
    context['friend_requests'] = FriendRequest.objects.filter(receiver=user, is_active=True)
    return render(request, 'friends/friend_requests.html', context)

@login_required(login_url='/login/')
def friend_list_view(request, *args, **kwargs):
    user = request.user
    context = {}
    friendlist = Friendlist.objects.get(user=user)
    friend_username = kwargs.get("username")
    if friend_username == None:
        username = '' 
    if request.GET:
            username = request.GET.get('username','')
            context['username'] = username
    if username == '' :
        friends = friendlist.friends.all()
    else :
        friends =  friendlist.friends.all().filter(username__contains=username)
    context['friends'] = friends
    return render(request, 'friends/friend_list.html', context)

"""
an ajax request that is used to send a friend_request from an authenticated user to another.
If the user already sent a previous request and it's active, we raise an exception
Else this function create a new request
"""
@login_required(login_url='/login/')
def send_friend_request(request):
    user = request.user
    payload = {}
    if request.method == 'POST' and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                #Get any friend requests(active and not-active)
                friend_requests = FriendRequest.objects.filter(sender=user,receiver=receiver)
                #find if any of them are active
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("You already sent them a friend request")
                    #if none are active, then create a new friend request
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    payload['response'] = "Friend request sent."
                except Exception as e:
                    payload['response'] = str(e)
            except FriendRequest.DoesNotExist:
                #There are no friend requests
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = "Friend request sent."

            if payload['response'] == None:
                payload['response'] = "Something went wrong."
        else:
            payload['response'] = "Unable to send a friend request."
    else:
            payload['response'] = "You must be authenticated."
    # if payload['response'] == "Friend request sent.":
    #     messages.success(request, f"Friend request sent to {receiver.username}.")
    # else:
    #     messages.warning(request, payload['response'])
    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required(login_url='/login/')
def cancel_friend_request(request):
    user = request.user
    payload = {}
    if request.method == 'POST' and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                #Get any friend requests(active and not-active)
                friend_requests = FriendRequest.objects.filter(sender=user,receiver=receiver,
                                                               is_active=True)
                if len(friend_requests) > 1 :
                        for request in friend_requests:
                            request.cancel()
                            payload['response'] = "Friend request cancelled."
                else:
                    friend_requests.first().cancel()
                    payload['response'] = "Friend request cancelled."
            except Exception:
                #There are no friend requests
                payload['response'] = "Nothing to cancel. Friend request does not exist."
        else:
            payload['response'] = "Unable to cancel your friend request."
    else:
            payload['response'] = "You must be authenticated."
    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required(login_url='/login/')
def accept_friend_request(request,*args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'GET' and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user :
                    if friend_request:
                        friend_request.accept()
                        payload['response'] = "Friend request accepted."
                    else:
                        payload['response'] = "Something went wrong."
            else:
                payload['response'] = "That is not your request to accept."
        else:
            payload['response'] = "Unable to accept that friend request."
    else:
        payload['response'] = "You must be authenticated."
    if payload['response'] == "Friend request accepted.":
        messages.success(request, f"{user.username}, you are now friends with {friend_request.sender.username}.")
    else:
        messages.warning(request, payload['response'])
    return HttpResponse(json.dumps(payload), content_type="application/json")

def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'GET' and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user :
                if friend_request:
                    friend_request.decline()
                    payload['response'] = "Friend request declined."
                else:
                    payload['response'] = "Something went wrong."
            else:
                    payload['response'] = "That is not your request to cancel."
    else:
        payload['response'] = "Unable to decline that friend request."
    if payload['response'] == "Friend request declined.":
        messages.success(request, f"Friend request declined successfully.")
    else:
        messages.warning(request, payload['response'])
    return HttpResponse(json.dumps(payload), content_type="application/json")

def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            try:
                removee =  User.objects.get(pk=user_id)
                friend_list = Friendlist.objects.get(user=user)
                friend_list.unfriend_user(removee=removee)
                payload['response'] = "Succesfully removed that friend."
            except Exception as e:
                payload['response'] = f"Something went wrong: {str(e)}"
        else:
            payload['response'] = "There was an error. Unable to remove that friend"
    else:
        payload['response'] = "You must be authenticated to remove a friend."
    if payload['response'] == "Succesfully removed that friend..":
        messages.success(request, f"Succesfully removed that friend.")
    else:
        messages.warning(request, payload['response'])
    return HttpResponse(json.dumps(payload), content_type="application/json")
