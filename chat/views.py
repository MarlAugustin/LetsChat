from django.shortcuts import render,redirect
from .models import PublicChatRoom, Message, PrivateChatRoom, PrivateMessage
from friends.models import Friendlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
#import for paginations
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
"""
This is the homepage where authenticated users can see all the public chat rooms
If the user is not authenticated, they are redirected to the login page
"""
ROOMS_PER_PAGE = 9
@login_required(login_url='/login/')
def home(request):
    #rooms = PublicChatRoom.objects.all().order_by('?')
    #rooms = PublicChatRoom.objects.all()
    
    #setting up pagination
    #The number inside of paginator represents how many elements will be shown in a page
    context = {}
    room_name = ''
    if request.GET:
            room_name = request.GET.get('room_name','')
            context['room_name'] = room_name
    if room_name == '' :
        query = PublicChatRoom.objects.all()
    else :
        query =  PublicChatRoom.objects.filter(name__contains=room_name)
    page = request.GET.get('page', 1)
    paginator = Paginator(query, ROOMS_PER_PAGE)
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(ROOMS_PER_PAGE)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)
    
    context['rooms'] = rooms

    return render(request,'home.html', context)

"""
This is the room view where the authenticated user can see all the messages in a specified chat room
"""
@login_required(login_url='/login/')
def room(request, slug):
    context = {}
    username = request.user.username
    try:
        room = PublicChatRoom.objects.get(slug=slug)
        chat_messages = Message.objects.filter(room=room)
        context['chat_messages'] = chat_messages
        context['room'] = room
    except Exception as e:
        # messages.warning(request, f'{username}, the public room that you tried to access did not exist.')
        # return redirect('home')
        return HttpResponse(f'{username}, the public room that you tried to access did not exist.')


    return render(request, 'chat/public/room.html', context)

"""
This is the create room view where the authenticated user can create a chat room
"""
@login_required(login_url='/login/')
def create_room(request):
    if request.method == 'POST':
        name = request.POST['room-name']
        slug = name.replace(' ', '_').lower()
        public = True
        username = request.user.username
        #print(slug,name,public)
        try:
            PublicChatRoom.objects.create(name=name,public=public,slug=slug)
            messages.success(request, f'{username}, your have successfuly created a chat room')
        except:
            messages.warning(request, f'{username}, the name chosen for the group already exists')
            #print(messages.warning(request, f'{username}, the name chosen for the group already exists'))
    return render(request, 'chat/public/create_room.html')

@login_required(login_url='/login/')
def private_rooms(request, *args, **kwargs):
    context = {}
    user = request.user
    rooms = PrivateChatRoom.objects.filter(members__id=user.id).order_by('-id')
    if kwargs.get("id"):
        room_id = kwargs.get("id")
        try:
            current_room = rooms.get(pk=room_id)
            members = current_room.members.all()
            chat_messages = PrivateMessage.objects.filter(room=current_room)
            context['chat_messages'] = chat_messages
            context['rooms'] = rooms
            context['current_room'] = current_room
            context['members'] = members
        except Exception as e:
            return HttpResponse("You cannot view, a private chat that you are not a member of.")
    else:
        if rooms.__len__() > 0:
            current_room = rooms.first()
            chat_messages = PrivateMessage.objects.filter(room=current_room)
            members = current_room.members.all()
            context['chat_messages'] = chat_messages
            context['rooms'] = rooms
            context['current_room'] = current_room
            context['members'] = members
        else:
            context['chat_messages'] = None
            context['rooms'] = None
            context['current_room'] = None
            context['members'] = None
    friends =  Friendlist.objects.get(user=user).friends.all()
    context['friends'] = friends

    #Creation of a new private group chat or updating an existing group chat
    if request.method == 'POST':
        selected_friends_name = request.POST.getlist('selected-friends',None)
        group_name =  request.POST.get('group-name')
        creator = request.user
        if len(selected_friends_name) != 0:
            new_private_room = PrivateChatRoom(name=group_name,creator=creator)
            new_private_room.save()
            new_private_room.members.add(creator)
            for name in selected_friends_name:
                creator_friendlist = Friendlist.objects.get(user=creator).friends.all()
                friend = creator_friendlist.get(username__contains=name)
                # print(friend)
                new_private_room.members.add(friend)
            new_private_room.save()
            return redirect('private_room')
        else:
            messages.warning(request, f'{creator.username}, you must select at least 1 friend to create a group')
    return render(request, 'chat/private-groups/dms.html', context )
