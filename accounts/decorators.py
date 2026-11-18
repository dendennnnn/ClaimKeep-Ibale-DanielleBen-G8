from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please log in to access this page.')
                return redirect_to_login(request.get_full_path())

            if request.user.role not in allowed_roles:
                messages.error(
                    request,
                    'Access denied: You are not authorized to view that role dashboard.'
                )
                return redirect('accounts:dashboard_redirect')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator