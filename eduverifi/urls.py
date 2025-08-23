"""
URL configuration for eduverifi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django_otp.admin import OTPAdminSite
from two_factor.urls import urlpatterns as tf_urls
from admin_login.views import account_redirect

# Replace the default admin site with OTP-protected admin
admin.site.__class__ = OTPAdminSite
admin.site.site_header = 'EduVerifi Admin'
admin.site.site_title = 'EduVerifi Admin Portal'

# Extract the two_factor patterns and namespace
tf_patterns, tf_namespace = tf_urls

# Create custom patterns with our redirect at the root
custom_patterns = [
    path('account/', account_redirect, name='account_home'),  # Our custom redirect
] + tf_patterns

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    # Include modified two_factor URLs with our custom redirect
    path('', include((custom_patterns, tf_namespace))),
]
