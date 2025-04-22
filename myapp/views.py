from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
import random
import json
from dotenv import load_dotenv
import os

from .forms import CustomUserCreationForm

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp_email(email, otp):
    subject = 'Password Reset OTP'
    message = f'Your OTP for password reset is: {otp}\nThis OTP will expire in 10 minutes.'
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
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
    # Load environment variables
    load_dotenv()
    
    context = {
        'env': {
            'TRADINGVIEW_API_KEY': os.getenv('TRADINGVIEW_API_KEY'),
            'TRADINGVIEW_API_SECRET': os.getenv('TRADINGVIEW_API_SECRET')
        }
    }
    return render(request, 'analytics.html', context)

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
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            if not email:
                return JsonResponse({
                    'success': False,
                    'message': 'Email is required'
                })

            try:
                user = User.objects.get(email=email)
                # Generate OTP
                otp = generate_otp()
                
                # Store OTP in session
                request.session['reset_otp'] = otp
                request.session['reset_email'] = email
                request.session.set_expiry(600)  # 10 minutes
                
                # Send OTP email
                if send_otp_email(email, otp):
                    return JsonResponse({
                        'success': True,
                        'message': 'Verification code sent successfully'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Failed to send verification code'
                    })
                    
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'No account exists with this email address'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            })
            
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

def verify_reset_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            code = data.get('code')
            
            stored_otp = request.session.get('reset_otp')
            stored_email = request.session.get('reset_email')
            
            if not stored_otp or not stored_email:
                return JsonResponse({
                    'success': False,
                    'message': 'Verification code has expired. Please request a new code.'
                })
            
            if email != stored_email:
                return JsonResponse({
                    'success': False,
                    'message': 'Email does not match the one used for code request'
                })
            
            if code != stored_otp:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid verification code'
                })
            
            # Code is valid
            return JsonResponse({
                'success': True,
                'message': 'Code verified successfully'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request data'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

def update_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            new_password = data.get('new_password')
            
            stored_email = request.session.get('reset_email')
            
            if not stored_email or email != stored_email:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid password reset request'
                })
            
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                
                # Clear session data
                del request.session['reset_otp']
                del request.session['reset_email']
                
                return JsonResponse({
                    'success': True,
                    'message': 'Password updated successfully'
                })
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'User not found'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request data'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })
