

from django import template 
  
register = template.Library() 
  
@register.filter() 
def remove_user(members, user):
    # I created this custom filter, because in private chats there was an extra comma if the connected
    #user was the last member in the group
    #https://www.youtube.com/watch?v=xuGk760Dza8 
    return members.exclude(username__contains=user)

@register.simple_tag
def define(val=None):
  #https://stackoverflow.com/questions/1070398/how-to-assign-a-value-to-a-variable-in-a-django-template
  return val

