from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .models import Destination, DestinationImage, DestinationReview
from .forms import DestinationForm, ReviewForm

class UserIsAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        destination = self.get_object()
        return self.request.user == destination.author

class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    ordering = ['-created_at']

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destinations/destination_detail.html'
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.destination = self.object
            review.author = request.user
            review.save()
            return redirect('destinations:destination_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(review_form=form))

class DestinationCreateView(LoginRequiredMixin, CreateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_form.html'
    success_url = reverse_lazy('destinations:destination_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # Guardar múltiples imágenes de la galería
        for image in self.request.FILES.getlist('gallery'):
            DestinationImage.objects.create(destination=self.object, image=image)
        return response

class DestinationUpdateView(LoginRequiredMixin, UserIsAuthorMixin, UpdateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in self.request.FILES.getlist('gallery'):
            DestinationImage.objects.create(destination=self.object, image=image)
        return response

    def get_success_url(self):
        return reverse('destinations:destination_detail', kwargs={'pk': self.object.pk})

class DestinationDeleteView(LoginRequiredMixin, UserIsAuthorMixin, DeleteView):
    model = Destination
    template_name = 'destinations/destination_confirm_delete.html'
    success_url = reverse_lazy('destinations:destination_list')

class UserDestinationsView(ListView):
    model = Destination
    template_name = 'destinations/user_destinations.html'
    context_object_name = 'destinations'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Destination.objects.filter(author=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_user'] = get_object_or_404(User, username=self.kwargs['username'])
        return context
