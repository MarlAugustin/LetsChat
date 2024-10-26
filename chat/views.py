from django.shortcuts import render,redirect
from .models import PublicChatRoom, Message
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    room = PublicChatRoom.objects.get(slug=slug)
    chat_messages = Message.objects.filter(room=room)
    auth_user = request.user
    return render(request, 'chat/public/room.html', { 'chat_messages' : chat_messages,'room':room, 'auth_user':auth_user})

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
        print(slug,name,public)
        #PublicChatRoom.objects.create(name=name,public=public,slug=slug)
        try:
            PublicChatRoom.objects.create(name=name,public=public,slug=slug)
            messages.success(request, f'{username}, your have successfuly created a chat room')
        except:
            messages.warning(request, f'{username}, the name chosen for the group already exists')
            #print(messages.warning(request, f'{username}, the name chosen for the group already exists'))
    return render(request, 'chat/public/create_room.html')

@login_required(login_url='/login/')
def private_rooms(request):
    rooms = PublicChatRoom.objects.all().order_by('-slug')
    return render(request, 'chat/private-groups/dms.html', {'rooms':rooms})
