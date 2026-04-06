from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, PostImage, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
# Listado de posts publicados

def home(request):
    return render(request, 'home.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-created_at')

# Detalle de un post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        # Usamos prefetch_related para optimizar la carga de comentarios y sus autores
        return super().get_queryset().filter(status=Post.Status.PUBLISHED).prefetch_related('comments__author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        # Los comentarios ya están en self.object.comments gracias a prefetch_related
        return context

    def post(self, request, *args, **kwargs):
        # Solo usuarios autenticados pueden comentar
        if not request.user.is_authenticated:
            return redirect('users:login')

        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect(self.object.get_absolute_url())
        
        return self.render_to_response(self.get_context_data(comment_form=form))

# Crear post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        # Asignar autor
        form.instance.author = self.request.user

        # Guardar el post
        response = super().form_valid(form)

        # Guardar imágenes asociadas
        for image in self.request.FILES.getlist('images'):
            PostImage.objects.create(post=self.object, image=image)

        print(f">>> Post creado: {self.object.title} (ID: {self.object.pk})")
        return response

    def form_invalid(self, form):
        print(">>> ERRORES FORM:", form.errors)
        return super().form_invalid(form)

# Editar post
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in self.request.FILES.getlist('images'):
            PostImage.objects.create(post=self.object, image=image)
        return response

class UserPostsView(ListView):
    """Muestra los posts de un usuario específico."""
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.view_user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=self.view_user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_user'] = self.view_user
        return context

class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina un post si el usuario es el autor."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('blog:user_posts', kwargs={'username': self.request.user.username})
