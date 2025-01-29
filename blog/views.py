from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import BlogPost
from .forms import BlogPostForm


class BlogBaseView(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_blog'] = True
        return context


class BlogPostListView(BlogBaseView, ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogPostDetailView(BlogBaseView, DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views_count += 1
        post.save(update_fields=['views_count'])
        return post


class BlogPostCreateView(BlogBaseView, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:all_posts')

    def form_valid(self, form):
        # Устанавливаем is_published в True или False в зависимости от состояния чекбокса
        form.instance.is_published = self.request.POST.get('is_published') == 'on'
        return super().form_valid(form)

    def form_invalid(self, form):
        # Если форма не валидна, возвращаем пользователя обратно с ошибками
        return self.render_to_response(self.get_context_data(form=form))


class BlogPostUpdateView(BlogBaseView, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:all_posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context


class BlogPostDeleteView(BlogBaseView, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:all_posts')

    def get(self, request, *args, **kwargs):
        # Переопределяем метод get для предотвращения доступа к удалению через GET-запрос
        return self.post(request, *args, **kwargs)


class HomePageView(BlogPostListView):
    template_name = 'blog/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:2]
        context['is_base'] = True
        return context

