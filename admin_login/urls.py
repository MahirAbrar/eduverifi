from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls
from . import views

app_name = 'admin_login'

# We need to include two_factor URLs with proper namespace
urlpatterns = [
    # Include all two_factor URLs (they expect 'two_factor' namespace)
    path('', include(tf_urls)),
    
    # Override the login to use our custom version if needed
    path('login/', views.AdminLoginView.as_view(), name='custom_login'),
]