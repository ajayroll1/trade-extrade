from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import JsonResponse

from .forms import CustomUserCreationForm

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp_email(email, otp):
    subject = 'Your OTP for Registration'
    message = f'Your OTP for registration is: {otp}\nThis OTP will expire in 10 minutes.'
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # From email from settings.py
            [email],  # To email (user's input email)
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            otp = generate_otp()
            # Store OTP in session
            request.session['signup_otp'] = otp
            request.session['signup_email'] = email
            request.session.set_expiry(600)  # OTP expires in 10 minutes
            
            if send_otp_email(email, otp):  # Send to the email provided in the form
                return JsonResponse({'success': True, 'message': 'OTP sent successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to send OTP'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        otp = request.POST.get('otp')
        stored_otp = request.session.get('signup_otp')
        stored_email = request.session.get('signup_email')
        
        if not stored_otp or not stored_email:
            messages.error(request, 'OTP verification required')
            return render(request, 'signup.html', {'form': form})
        
        if otp != stored_otp:
            messages.error(request, 'Invalid OTP')
            return render(request, 'signup.html', {'form': form})
        
        if form.is_valid() and form.cleaned_data['email'] == stored_email:
            user = form.save()
            # Clear session data
            del request.session['signup_otp']
            del request.session['signup_email']
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Print for debugging
        print(f"Login attempt - Username: {username}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def wishlist(request):
    return render(request, 'wishlist.html')

@login_required
def trades(request):
    return render(request, 'trades.html')

@login_required
def analytics(request):
    return render(request, 'analytics.html')

@login_required
def signal(request):
    return render(request, 'signal.html')

@login_required
def pamm(request):
    return render(request, 'pamm.html')

@login_required
def history(request):
    return render(request, 'history.html')

def send_reset_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        
        try:
            user = User.objects.get(email=email)
            # Generate 6-digit code
            verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            # In a real application, you would send this code via email
            # For now, we'll just return it in the response
            print(f"Verification code for {email}: {verification_code}")
            
            # You should store this code in the database with an expiration time
            # For now, we'll just send it back to verify on the client side
            return JsonResponse({
                'success': True,
                'code': verification_code  # In production, don't send the code back directly
            })
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'No account found with this email address'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def update_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')
        new_password = data.get('new_password')
        
        try:
            user = User.objects.get(email=email)
            # In a real application, you would verify the code against what's stored in the database
            # For now, we'll just update the password
            user.set_password(new_password)
            user.save()
            
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'User not found'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
