from django.urls import path
from .views import UserCreateView, UserUpdatedView, UserDetailView,  LogoutView  , LoginView # to make user sign up, update, detail, restaurant list
 
app_name = 'accounts'

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('profile/edit/', UserUpdatedView.as_view(), name='edit_profile'),
    path('login/', LoginView.as_view(), name='login'),
    
]