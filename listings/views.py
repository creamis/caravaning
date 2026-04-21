from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from .models import Listing, ListingImage, Review
from .forms import ListingForm, ReviewForm
User = get_user_model()


class UserIsOwnerMixin(UserPassesTestMixin):
    """Verifica que el usuario que hace la petición es el propietario del objeto."""
    def test_func(self):
        return self.request.user == self.get_object().owner

class ExternalRentalsView(TemplateView):
    """Muestra información sobre plataformas de alquiler externas (afiliados)."""
    template_name = 'listings/external_rentals.html'

class ListingListView(ListView):
    model = Listing
    template_name = 'listings/listing_list.html'
    context_object_name = 'listings'
    paginate_by = 6

    def get_queryset(self):
        # Empezamos con todos los anuncios disponibles
        queryset = Listing.objects.filter(is_available=True).prefetch_related('images', 'likes').order_by('-created_at')
        
        # Obtenemos los parámetros de filtrado desde la URL (GET)
        location = self.request.GET.get('location')
        listing_type = self.request.GET.get('listing_type')
        category = self.request.GET.get('category')
        seller_type = self.request.GET.get('seller_type') # Nuevo filtro
        max_price = self.request.GET.get('max_price')

        if location:
            queryset = queryset.filter(location__icontains=location)
        if listing_type:
            queryset = queryset.filter(listing_type=listing_type)
        if category:
            queryset = queryset.filter(category=category)
        if seller_type: # Aplicar filtro de tipo de vendedor
            queryset = queryset.filter(seller_type=seller_type)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        return queryset


class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'
    context_object_name = 'listing'

    def get_queryset(self):
        # Optimizamos la carga de reseñas y sus autores para evitar consultas N+1
        return super().get_queryset().prefetch_related('reviews__author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Solo creamos un formulario nuevo si no viene uno con errores del método POST
        if 'review_form' not in context:
            context['review_form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')

        self.object = self.get_object()
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.listing = self.object
            review.author = request.user
            review.save()
            return redirect('listings:listing_detail', pk=self.object.pk)
        
        return self.render_to_response(self.get_context_data(review_form=form))


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'

    def form_valid(self, form):
        # Asignar el usuario actual como propietario del anuncio
        form.instance.owner = self.request.user
        self.object = form.save()

        # Procesar las imágenes subidas
        for image in self.request.FILES.getlist('images'):
            ListingImage.objects.create(listing=self.object, image=image)
        
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir a la página de detalle del anuncio recién creado
        return reverse('listings:listing_detail', kwargs={'pk': self.object.pk})


class ListingUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'

    def get_success_url(self):
        return reverse('listings:listing_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Permite añadir nuevas imágenes al editar.
        for image in self.request.FILES.getlist('images'):
            ListingImage.objects.create(listing=self.object, image=image)
        return super().form_valid(form)

class ListingDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Listing
    template_name = 'listings/listing_confirm_delete.html'
    
    def get_success_url(self):
        # Redirige a la lista de anuncios del usuario tras eliminar uno.
        return reverse_lazy('listings:user_listings', kwargs={'username': self.request.user.username})


class UserListingsView(ListView):
    """
    Muestra todos los anuncios de un usuario específico.
    """
    model = Listing
    template_name = 'listings/user_listings.html'
    context_object_name = 'listings'

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, username=self.kwargs['username'])
        return Listing.objects.filter(owner=self.profile_user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.profile_user
        return context

def toggle_like(request, pk):
    """Añade o elimina un like de un anuncio."""
    if not request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'authenticated': False}, status=401)
        return redirect('users:login')
    
    listing = get_object_or_404(Listing, pk=pk)
    is_liked = listing.likes.filter(id=request.user.id).exists()
    
    if is_liked:
        listing.likes.remove(request.user)
    else:
        listing.likes.add(request.user)
    
    # Si es una petición AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': not is_liked,
            'likes_count': listing.likes.count()
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'listings:listing_list'))