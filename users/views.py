from django.shortcuts import render,redirect
from .forms import SignUpForm, UpdateUserForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.
"""
This is the profile view where the user can update their profile
If the forms are valid, the user informations are updated and a success message is displayed
Else the form errors are displayed
"""
@login_required(login_url='/users/login/')
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
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request,'users/profile.html', context)

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
            return redirect('login')
        else: 
            messages.warning(request,form.errors)

    else: 
        form = SignUpForm()
    return render(request, 'users/register.html',{'form':form})
