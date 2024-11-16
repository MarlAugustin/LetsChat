from django.urls import path, include
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('friend_remove/',views.remove_friend, name="remove-friend"),
    path('friend_requests/',views.friend_requests_view, name="friend-requests"),
    path('friend_list/',views.friend_list_view, name="friend-list"),
    path('send_friend_request/',views.send_friend_request, name="send-friend-request"),
    path('cancel_friend_request/',views.cancel_friend_request, name="cancel-friend-request"),
    path('accept_friend_request/<int:friend_request_id>',views.accept_friend_request, name="accept-friend-request"),
    path('decline_friend_request/<int:friend_request_id>',views.decline_friend_request, name="decline-friend-request")
]
