from django.urls import path
from .views import (MenuItemListView, MenuItemDetailView, MenuItemCreateView,
                   MenuItemUpdateView, MenuItemDeleteView
                   )

app_name = 'menu'

urlpatterns = [
    path('', MenuItemListView.as_view(), name='list'),
    path('create/', MenuItemCreateView.as_view(), name='create'),
    path('<int:pk>/', MenuItemDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', MenuItemUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', MenuItemDeleteView.as_view(), name='delete') 
    
    
]