from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from basic_app.models import Post,Comment
from basic_app.forms import PostForm,CommentForm

# Create your views here.
#### Post views ##########
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'basic_app/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'basic_app/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    success_url = reverse_lazy('post_list')
    model = Post

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'basic_app/post_detail.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-create_date')

@login_required
def publish_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

########### Comment Views #############
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'basic_app/comment_form.html',{'form':form})

@login_required
def approve_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def delete_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
