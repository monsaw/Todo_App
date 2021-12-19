from django.shortcuts import render
from django.views.generic.edit import DeleteView
from .models import Task 
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CustomisedLogin(LoginView):
    template_name = 'base_app/login.html'
    fields = '__all__'
    redirect_authenticated_user =True

    def get_success_url(self):
        return reverse_lazy('list')

class RegisterPage(FormView):
    template_name = 'base_app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('list')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage , self).form_valid(form)
        

class TaskList(ListView):
    model = Task

    # def get_queryset(self):
    #     return Task.objects.filter(user = self.request.user)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = context['object_list'].filter(user = self.request.user)
        context['count'] = context['object_list'].filter(complete = False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['object_list'] = context['object_list'].filter(title__startswith =search_input)
        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task

class TaskCreate(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'base_app/task_detail.html'
    model = Task
    fields = ['title','description','complete','created']
    success_url = reverse_lazy('list')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'base_app/task_detail.html'
    model = Task
    fields = ['title','description','complete','created']
    success_url = reverse_lazy('list')

class TaskDelete(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    redirect_field_name = 'base_app/task_detail.html'
    model = Task
    success_url = reverse_lazy('list')