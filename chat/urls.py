from django.urls import path, include
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('create_room/',views.create_room, name='create_room'),
    path('private/',views.private_rooms, name='private_room'),
    path('private/<int:id>',views.private_rooms, name='private_room'),
    path('public/<slug:slug>/',views.room, name='room'),
]
