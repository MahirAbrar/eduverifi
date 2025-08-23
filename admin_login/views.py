from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from two_factor.views import LoginView
from two_factor.utils import default_device


def account_redirect(request):
    """
    Smart redirect for /account/ based on user's authentication status.
    """
    print(f"DEBUG: account_redirect called, user authenticated: {request.user.is_authenticated}")
    
    if not request.user.is_authenticated:
        # Not logged in -> go to login
        print("DEBUG: Redirecting to login")
        return redirect('/account/login/')
    
    if not default_device(request.user):
        # Logged in but no 2FA -> go to setup
        messages.info(request, "Please set up two-factor authentication for enhanced security.")
        return redirect('/account/two_factor/setup/')
    
    # Logged in with 2FA -> go to profile
    return redirect('/account/two_factor/')


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