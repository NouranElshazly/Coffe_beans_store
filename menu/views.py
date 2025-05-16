from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import MenuItem 
from .forms import MenuItemForm 
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to restrict access to admin users only"""
    def test_func(self):
        return self.request.user.is_admin  # Using your is_admin property
    
    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('home')

class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'menu/menuitem_list.html'
    context_object_name = 'menu_items'
    
    def get_queryset(self):
        # Show all items to admin users
        return MenuItem.objects.all()

class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'menu/menuitem_detail.html'

class MenuItemCreateView(AdminRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu/menuitem_form.html'
    success_url = reverse_lazy('menu:list')

    def form_valid(self, form):
        # Remove restaurant assignment since only admin can create
        return super().form_valid(form)

class MenuItemUpdateView(AdminRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu/menuitem_form.html'
    success_url = reverse_lazy('menu:list')

class MenuItemDeleteView(AdminRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'menu/menuitem_confirm_delete.html'
    success_url = reverse_lazy('menu:list')

# class CategoryListView(ListView):
#     model = Category
#     template_name = 'menu/category_list.html'

# class CategoryCreateView(AdminRequiredMixin, CreateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = 'menu/category_form.html'
#     success_url = reverse_lazy('menu:category_list')