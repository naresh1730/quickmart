from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm,UserUpdateForm, ProfileUpdateForm
# Create your views here.

def signup_view(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,"Account created successfully")
            return redirect('profile')
        else:
            messages.error(request,'please check entered details')
    else:
        form=SignUpForm()
    return render(request,'accounts/signup.html', {'form':form})

def login_view(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('cart:view_cart')
        else:
            messages.error(request,'Invalid credentials')
    return render(request,'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    if request.method=="POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'profile updated successfully')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
        context={
            'u_form': u_form,
            'p_form': p_form,
        }
    return render(request,'accounts/profile.html', context)