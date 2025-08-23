from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls
from . import views

app_name = 'admin_login'

urlpatterns = [
    # Smart redirect for /account/ based on authentication status
    path('', views.account_redirect, name='account_redirect'),
    
    # Include all two_factor URLs (they come as a tuple with namespace)
    path('', include(tf_urls)),
    
    # Override the login to use our custom version if needed
    path('login/', views.AdminLoginView.as_view(), name='custom_login'),
]