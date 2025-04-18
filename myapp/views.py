from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Add any other imports you need

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Changed from 'home' to 'dashboard'
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
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
