from django.shortcuts import redirect
from django.urls import reverse
from two_factor.utils import default_device


class EnforceTwoFactorMiddleware:
    """
    Middleware to enforce 2FA setup for authenticated users trying to access admin.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip middleware for auth-related paths
        exempt_paths = ['/account/', '/static/']
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)
        
        # Check if user is authenticated and trying to access admin
        if request.user.is_authenticated and request.path.startswith('/admin/'):
            # Check if user has 2FA set up
            if not default_device(request.user):
                # Redirect to 2FA setup if not configured
                return redirect(reverse('two_factor:setup'))
        
        response = self.get_response(request)
        return response