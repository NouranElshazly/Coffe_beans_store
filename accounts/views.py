from django.shortcuts import render , redirect
from django.views.generic import CreateView, UpdateView, ListView , View, DetailView
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth.views import  LoginView  , LogoutView   
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Cart
from checkout.models import Order

# Create your views here.
class UserCreateView(CreateView):   # to make user sign up 
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html' 

    success_url = reverse_lazy('login')
    def form_valid(self, form):
        user =form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfully')
        return redirect('accounts:login')
        

    def form_invalid(self, form):
        # Add error messages for invalid form
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
     
# to update user informations
class UserUpdatedView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)

     # to appeared user informations  
class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'  # Changed from user_detail.html
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart.objects.filter(user=self.request.user, completed=False).first()
        context['orders'] = Order.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        return context
    

class LoginView( LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:profile')


class LogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')
