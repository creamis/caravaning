from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, forms as auth_forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile  # Asegúrate de importar el modelo Profile
from .forms import CustomUserCreationForm, ProfileUpdateForm
from listings.models import Listing
from blog.models import Post
from destinations.models import Destination
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.urls import reverse


def safe_return_url(request):
    """Permite regresar únicamente a una URL interna segura."""
    from django.utils.http import url_has_allowed_host_and_scheme

    destination = (
        request.POST.get("next")
        or request.GET.get("next")
        or ""
    )

    if url_has_allowed_host_and_scheme(
        url=destination,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return destination

    return ""

def register(request):
    """Vista para registrar nuevos usuarios."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data["email"]
            user.save()
            login(request, user)  # Inicia sesión automáticamente al registrarse
            return redirect(safe_return_url(request) or 'home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form, 'next': safe_return_url(request)})

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

@never_cache
def login_view(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if request.user.is_authenticated:
        return redirect(safe_return_url(request) or "home")

    form = auth_forms.AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            destination = safe_return_url(request) or "/"

            if is_ajax:
                return JsonResponse({
                    "success": True,
                    "destination": destination,
                })

            return redirect(destination)

        if is_ajax:
            return JsonResponse({
                "success": False,
                "error": "Usuario o contraseña incorrectos.",
            }, status=400)

        messages.error(
            request,
            "Por favor, revisa los datos introducidos."
        )

    return render(
        request,
        "users/login.html",
        {
            "form": form,
            "next": safe_return_url(request),
        },
    )

@require_POST
def logout_view(request):
    destination = safe_return_url(request) or reverse("home")
    logout(request)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "destination": destination,
        })

    return redirect(destination)


def public_profile(request, username):
    from django.contrib.auth import get_user_model
    from django.shortcuts import get_object_or_404, render
    from community.models import Publication

    User = get_user_model()

    traveler = get_object_or_404(
        User,
        username=username,
        is_active=True,
    )

    publications = (
        Publication.objects
        .filter(
            author=traveler,
            status="PUBLISHED",
        )
        .prefetch_related("images")
        .order_by("-created_at")
    )

    return render(
        request,
        "users/public_profile.html",
        {
            "traveler": traveler,
            "publications": publications,
            "publication_count": publications.count(),
        },
    )


def public_profile(request, username):
    from django.contrib.auth import get_user_model
    from django.shortcuts import get_object_or_404, render
    from community.models import Publication

    User = get_user_model()

    traveler = get_object_or_404(
        User,
        username=username,
        is_active=True,
    )

    publications = (
        Publication.objects
        .filter(
            author=traveler,
            status="PUBLISHED",
        )
        .prefetch_related("images")
        .order_by("-created_at")
    )

    return render(
        request,
        "users/public_profile.html",
        {
            "traveler": traveler,
            "publications": publications,
            "publication_count": publications.count(),
        },
    )
