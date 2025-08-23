from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from two_factor.views import LoginView
from two_factor.utils import default_device


class AdminLoginView(LoginView):
    """
    Custom login view that enforces 2FA setup for admin access.
    Inherits from two_factor LoginView to maintain all 2FA functionality.
    """
    
    def get_success_url(self):
        """Redirect to 2FA setup if not configured, otherwise to admin."""
        # Get the redirect URL from the request first
        redirect_to = self.request.GET.get('next', '')
        
        # If user doesn't have 2FA set up, force them to set it up
        if not default_device(self.request.user):
            messages.warning(self.request, "Please set up two-factor authentication to access the admin panel.")
            return reverse('two_factor:setup')
        
        # Otherwise redirect to the requested page or admin
        return redirect_to or '/admin/'


@login_required
def enforce_2fa(request):
    """
    Helper view to enforce 2FA setup before accessing admin.
    Redirects to setup if not configured, otherwise to admin.
    """
    if not default_device(request.user):
        messages.warning(request, "Please set up two-factor authentication to access the admin panel.")
        return redirect('two_factor:setup')
    return redirect('/admin/')