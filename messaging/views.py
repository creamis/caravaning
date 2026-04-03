from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from .forms import ContactSellerForm

@login_required
def contact_seller(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    if request.method == 'POST':
        form = ContactSellerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Cuerpo del correo
            subject = f"Consulta sobre tu anuncio: {listing.title}"
            full_message = f"Hola {listing.owner.username},\n\nHas recibido una consulta de {name} ({email}) sobre tu anuncio '{listing.title}':\n\n{message}"
            
            try:
                send_mail(
                    subject,
                    full_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [listing.owner.email],
                    fail_silently=False,
                )
                messages.success(request, "Tu mensaje ha sido enviado correctamente al vendedor.")
                return redirect('listings:listing_detail', pk=listing.pk)
            except Exception:
                messages.error(request, "Hubo un error al enviar el email. Inténtalo de nuevo más tarde.")
    else:
        # Pre-rellenamos los datos si el usuario está logueado
        initial_data = {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email
        }
        form = ContactSellerForm(initial=initial_data)
        
    return render(request, 'messaging/contact_form.html', {
        'form': form,
        'listing': listing
    })