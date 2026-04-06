from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, forms as auth_forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile  # Asegúrate de importar el modelo Profile
from .forms import CustomUserCreationForm, ProfileUpdateForm
from listings.models import Listing
from blog.models import Post
from destinations.models import Destination

def register(request):
    """Vista para registrar nuevos usuarios."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data["email"]
            user.save()
            login(request, user)  # Inicia sesión automáticamente al registrarse
            return redirect('home')  # Redirige a la página de inicio
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    context = {
        'listing_count': Listing.objects.filter(owner=request.user).count(),
        'post_count': Post.objects.filter(author=request.user).count(),
        'destination_count': Destination.objects.filter(author=request.user).count(),
    }
    
    return render(request, "users/profile.html", context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile_edit.html', {'form': form})

def login_view(request):
    form = auth_forms.AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
        else:
            messages.error(request, "Por favor, revisa los datos introducidos.")
            
    return render(request, "users/login.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect("home")
