from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import role_required
from .forms import AccountRegistrationForm, AccountLoginForm, UserProfileUpdateForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')

    if request.method == 'POST':
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f'Account created successfully for {user.full_name}! You may now log in.'
            )
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the highlighted errors below.')
    else:
        form = AccountRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')

    if request.method == 'POST':
        form = AccountLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name}!')
            return redirect('accounts:dashboard_redirect')
        else:
            messages.error(request, 'Invalid email address or password. Please try again.')
    else:
        form = AccountLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been securely logged out.')
        return redirect('accounts:login')
    return redirect('accounts:dashboard_redirect')


@login_required
def dashboard_redirect_view(request):
    if request.user.role == User.Role.ADMIN:
        return redirect('accounts:admin_dashboard')
    return redirect('accounts:consumer_dashboard')


@role_required([User.Role.CONSUMER])
def consumer_dashboard_view(request):
    context = {
        'total_purchases': 0,
        'total_spending': '0.00',
        'active_warranties': 0,
        'expiring_soon_warranties': 0,
        'expired_warranties': 0,
    }
    return render(request, 'accounts/consumer_dashboard.html', context)


@role_required([User.Role.ADMIN])
def admin_dashboard_view(request):
    total_users = User.objects.count()
    consumer_count = User.objects.filter(role=User.Role.CONSUMER).count()
    admin_count = User.objects.filter(role=User.Role.ADMIN).count()
    recent_users = User.objects.order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'consumer_count': consumer_count,
        'admin_count': admin_count,
        'recent_users': recent_users,
        'default_categories': [
            'Electronics',
            'Home Appliances',
            'Gadgets & Mobile',
            'Computer Hardware',
            'Furniture & Fixtures',
        ],
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile details have been updated.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Could not update profile. Please check the errors below.')
    else:
        form = UserProfileUpdateForm(instance=user)

    return render(request, 'accounts/profile.html', {'form': form})