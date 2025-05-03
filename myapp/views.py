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
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os
from django.views.decorators.http import require_http_methods
from decimal import Decimal, InvalidOperation
import logging
from django.db.models import Count, Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import TruncMonth

from .forms import CustomUserCreationForm
from .models import Trade, WishlistItem

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

        # First check if user exists and is active
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                messages.error(request, 'Your account is inactive. Please contact support for assistance.')
                return render(request, 'login.html')
        except User.DoesNotExist:
            # Don't reveal that the user doesn't exist
            pass

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:  # Check if user is admin
                return redirect('admin_dashboard')  # Redirect to admin panel dashboard
            else:
                return redirect('dashboard')  # Redirect to regular dashboard
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
    # Get all wishlist items for the current user
    wishlist_items = WishlistItem.objects.filter(user=request.user).order_by('-added_at')
    
    # Get OANDA credentials from environment variables
    oanda_api_key = os.getenv('FOREX_API_KEY')
    oanda_account_id = os.getenv('OANDA_ACCOUNT_ID')
    
    context = {
        'wishlist_items': wishlist_items,
        'FOREX_API_KEY': oanda_api_key,
        'OANDA_ACCOUNT_ID': oanda_account_id
    }
    
    return render(request, 'wishlist.html', context)

@login_required
@require_http_methods(["POST"])
def add_to_wishlist(request):
    try:
        data = json.loads(request.body)
        symbol = data.get('symbol')
        price = data.get('price')
        category = data.get('category')

        if not symbol or not category:
            return JsonResponse({
                'success': False,
                'message': 'Symbol and category are required'
            })

        # Convert price to Decimal
        if price:
            price = Decimal(str(price))

        # Map frontend category names to model choices
        category_map = {
            'Crypto': 'CRYPTO',
            'Stocks': 'STOCKS',
            'Indices': 'INDICES',
            'Commodities': 'COMMODITIES',
            'Forex': 'FOREX'
        }

        db_category = category_map.get(category, 'CRYPTO')

        # Check if item already exists
        wishlist_item, created = WishlistItem.objects.get_or_create(
            user=request.user,
            symbol=symbol,
            defaults={
                'category': db_category,
                'last_price': price,
                'price_change': 0
            }
        )

        if not created:
            # Update price if item already exists
            wishlist_item.last_price = price
            wishlist_item.save()
            message = 'Wishlist item updated'
        else:
            message = 'Added to wishlist'

        return JsonResponse({
            'success': True,
            'message': message,
            'item_id': wishlist_item.id
        })

    except Exception as e:
        print(f"Error adding to wishlist: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Failed to add item to wishlist'
        })

@csrf_exempt
def remove_from_wishlist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            print(f"Deleting item with ID: {item_id}")  # Debug print
            
            # Delete the item from database
            WishlistItem.objects.filter(id=item_id).delete()
            
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error deleting item: {str(e)}")  # Debug print
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

@login_required
def trades(request):
    # Get active trades for the current user, ordered by creation date (newest first)
    trades = Trade.objects.filter(user=request.user, status='active').order_by('-created_at')[:50]  # Limit to 50 trades

    # Initialize prices and profits
    for trade in trades:
        trade.current_price = None  # Will be updated via WebSocket
        trade.live_profit = 0.0     # Will be updated via WebSocket

    return render(request, 'trades.html', {'trades': trades})

def get_current_price(symbol):
    """
    Get current price from Binance API
    """
    import requests

    logger = logging.getLogger(__name__)

    try:
        # Convert symbol to Binance format if needed
        binance_symbol = symbol.replace('/', '')
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={binance_symbol}'

        logger.info(f"Fetching price for {binance_symbol} from {url}")
        response = requests.get(url, timeout=5)  # Add timeout

        if response.status_code == 200:
            data = response.json()
            price = float(data['price'])
            logger.info(f"Successfully fetched price for {binance_symbol}: {price}")
            return price
        else:
            error_msg = f"Error fetching price for {binance_symbol}: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return None
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching price for {binance_symbol}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while fetching price for {binance_symbol}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while fetching price for {binance_symbol}: {e}")
        return None

def calculate_live_profit(trade):
    # This will be implemented in the WebSocket consumer
    return None

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
    # Get all trades for the current user, ordered by creation date (newest first)
    trades = Trade.objects.filter(user=request.user).order_by('-created_at')

    # Calculate summary statistics
    total_trades = trades.count()
    total_profit = sum(float(trade.profit) for trade in trades)

    # Calculate win rate
    winning_trades = trades.filter(profit__gt=0).count()
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

    return render(request, 'history.html', {
        'trades': trades,
        'total_profit': total_profit,
        'win_rate': win_rate
    })

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

@login_required
@require_http_methods(["POST"])
def execute_trade(request):
    try:
        data = json.loads(request.body)

        # Calculate total amount (quantity * entry_price)
        quantity = float(data['quantity'])
        entry_price = float(data['price'])
        total_amount = quantity * entry_price

        # Create new trade
        trade = Trade.objects.create(
            user=request.user,
            symbol=data['symbol'],
            type=data['type'],
            quantity=data['quantity'],
            entry_price=data['price'],
            total_amount=total_amount,  # Add the calculated total amount
            status='active',  # Changed from 'closed' to 'active'
            stop_loss=data['stopLoss'],
            take_profit=data['takeProfit']
        )

        return JsonResponse({
            'success': True,
            'message': 'Trade executed successfully',
            'trade_id': trade.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def get_live_profit(request):
    print("\n=== Live Profit API Call ===")
    print(f"User: {request.user}")
    print(f"Request Method: {request.method}")

    try:
        # Get all active trades for the current user
        trades = Trade.objects.filter(user=request.user, status='active')
        print(f"Found {trades.count()} active trades")

        if trades.count() == 0:
            print("No active trades found")
            return JsonResponse({
                'success': True,
                'profits': []
            })

        profits = []
        for trade in trades:
            try:
                print(f"\nProcessing Trade {trade.id}:")
                print(f"Symbol: {trade.symbol}")
                print(f"Type: {trade.type}")
                print(f"Quantity: {trade.quantity}")
                print(f"Entry Price: {trade.entry_price}")

                # Get current price from Binance API
                current_price = get_current_price(trade.symbol)
                print(f"Current Price: {current_price}")

                if current_price is None:
                    print("Could not get current price, skipping trade")
                    continue

                # Calculate live profit
                if trade.type == 'BUY':
                    live_profit = (Decimal(str(current_price)) - trade.entry_price) * trade.quantity
                else:  # SELL
                    live_profit = (trade.entry_price - Decimal(str(current_price))) * trade.quantity

                print(f"Calculated Live Profit: {live_profit}")

                profits.append({
                    'trade_id': trade.id,
                    'current_price': current_price,
                    'live_profit': float(live_profit)
                })
            except Exception as trade_error:
                print(f"Error processing trade {trade.id}: {trade_error}")
                continue

        print(f"\nReturning {len(profits)} profit updates")
        return JsonResponse({
            'success': True,
            'profits': profits
        })
    except Exception as e:
        print(f"Error in get_live_profit: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@require_http_methods(["POST"])
def update_wishlist_price(request):
    try:
        data = json.loads(request.body)
        symbol = data.get('symbol')
        price = data.get('price')
        price_change = data.get('price_change')

        if not symbol or price is None:
            return JsonResponse({
                'success': False,
                'message': 'Symbol and price are required'
            })

        # Convert price to Decimal
        if price:
            price = Decimal(str(price))

        if price_change:
            price_change = Decimal(str(price_change))

        # Find and update the item
        try:
            wishlist_item = WishlistItem.objects.get(user=request.user, symbol=symbol)
            wishlist_item.last_price = price
            if price_change is not None:
                wishlist_item.price_change = price_change
            wishlist_item.save()

            return JsonResponse({
                'success': True,
                'message': 'Price updated'
            })
        except WishlistItem.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Item not found in wishlist'
            })

    except Exception as e:
        print(f"Error updating wishlist price: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Failed to update price'
        })

@login_required
@require_http_methods(["POST"])
def close_trade(request):
    try:
        data = json.loads(request.body)
        trade_id = data.get('trade_id')
        closing_price = data.get('closing_price')

        if not trade_id:
            return JsonResponse({
                'success': False,
                'error': 'Trade ID is required'
            })

        try:
            # Get the trade
            trade = Trade.objects.get(id=trade_id, user=request.user)
            
            # Calculate profit
            if trade.type == 'BUY':
                profit = (Decimal(str(closing_price)) - trade.entry_price) * trade.quantity
            else:  # SELL
                profit = (trade.entry_price - Decimal(str(closing_price))) * trade.quantity
            
            # Update trade - these changes will make the trade appear in history
            trade.closing_price = Decimal(str(closing_price))
            trade.profit = profit
            trade.status = 'closed'  # Mark as closed
            trade.closed_at = datetime.now(timezone.utc)
            trade.save()

            # The trade will now automatically appear in the history page
            # since the history view shows all trades regardless of status

            return JsonResponse({
                'success': True,
                'message': 'Trade closed successfully',
                'trade_id': trade.id,
                'profit': float(profit)
            })
        except Trade.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Trade not found'
            })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@require_http_methods(["POST"])
def update_sltp(request):
    try:
        data = json.loads(request.body)
        trade_id = data.get('trade_id')
        stop_loss = data.get('stop_loss')
        take_profit = data.get('take_profit')

        if not trade_id:
            return JsonResponse({
                'success': False,
                'error': 'Trade ID is required'
            })

        try:
            # Get the trade
            trade = Trade.objects.get(id=trade_id, user=request.user, status='active')
            
            # Update stop loss and take profit values
            if stop_loss:
                trade.stop_loss = Decimal(str(stop_loss))
            else:
                trade.stop_loss = None
                
            if take_profit:
                trade.take_profit = Decimal(str(take_profit))
            else:
                trade.take_profit = None
                
            trade.save()

            return JsonResponse({
                'success': True,
                'message': 'Stop Loss and Take Profit updated successfully',
                'trade_id': trade.id,
                'stop_loss': float(trade.stop_loss) if trade.stop_loss else None,
                'take_profit': float(trade.take_profit) if trade.take_profit else None
            })
        except Trade.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Trade not found or not active'
            })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@require_http_methods(["POST"])
def update_trade_status(request):
    try:
        data = json.loads(request.body)
        trade_id = data.get('trade_id')
        current_price = data.get('current_price')

        if not trade_id or current_price is None:
            return JsonResponse({
                'success': False,
                'error': 'Trade ID and current price are required'
            })

        try:
            # Get the trade
            trade = Trade.objects.get(id=trade_id, user=request.user, status='active')
            
            # Convert current price to Decimal
            current_price = Decimal(str(current_price))
            
            # Check if stop loss or take profit has been triggered
            status_changed = False
            message = ""
            
            if trade.type == 'BUY':
                # For BUY trades, stop loss is triggered when price falls below stop loss level
                if trade.stop_loss and current_price <= trade.stop_loss:
                    trade.status = 'closed'
                    trade.closing_price = trade.stop_loss
                    trade.profit = (trade.stop_loss - trade.entry_price) * trade.quantity
                    trade.closed_at = datetime.now(timezone.utc)
                    status_changed = True
                    message = "Stop Loss triggered"
                
                # For BUY trades, take profit is triggered when price rises above take profit level
                elif trade.take_profit and current_price >= trade.take_profit:
                    trade.status = 'closed'
                    trade.closing_price = trade.take_profit
                    trade.profit = (trade.take_profit - trade.entry_price) * trade.quantity
                    trade.closed_at = datetime.now(timezone.utc)
                    status_changed = True
                    message = "Take Profit triggered"
            
            else:  # SELL trade
                # For SELL trades, stop loss is triggered when price rises above stop loss level
                if trade.stop_loss and current_price >= trade.stop_loss:
                    trade.status = 'closed'
                    trade.closing_price = trade.stop_loss
                    trade.profit = (trade.entry_price - trade.stop_loss) * trade.quantity
                    trade.closed_at = datetime.now(timezone.utc)
                    status_changed = True
                    message = "Stop Loss triggered"
                
                # For SELL trades, take profit is triggered when price falls below take profit level
                elif trade.take_profit and current_price <= trade.take_profit:
                    trade.status = 'closed'
                    trade.closing_price = trade.take_profit
                    trade.profit = (trade.entry_price - trade.take_profit) * trade.quantity
                    trade.closed_at = datetime.now(timezone.utc)
                    status_changed = True
                    message = "Take Profit triggered"
            
            # Save trade if status changed
            if status_changed:
                # Saving the trade with 'closed' status and profit will make it appear in history
                trade.save()
                return JsonResponse({
                    'success': True,
                    'status_changed': True,
                    'message': message,
                    'trade_id': trade.id,
                    'profit': float(trade.profit)
                })
            
            return JsonResponse({
                'success': True,
                'status_changed': False,
                'trade_id': trade.id
            })
                
        except Trade.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Trade not found or not active'
            })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@staff_member_required
def admin_dashboard(request):
    total_traders = User.objects.count()
    active_trades = Trade.objects.filter(status='active').count()
    
    # Calculate total trading volume
    total_volume = Trade.objects.filter(status='closed').aggregate(total=Sum('total_amount'))['total'] or 0
    volume_in_millions = total_volume / 1000000

    # Get last 6 months of trading volume data
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_volumes = Trade.objects.filter(
        created_at__gte=six_months_ago,
        status='closed'
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        volume=Sum('total_amount')
    ).order_by('month')

    # Format data for the chart
    volume_data = {
        'labels': [],
        'volumes': []
    }
    
    for entry in monthly_volumes:
        volume_data['labels'].append(entry['month'].strftime('%b %Y'))
        volume_data['volumes'].append(float(entry['volume']) / 1000000)  # Convert to millions

    return render(request, 'admin_dashboard.html', {
        'total_traders': total_traders,
        'active_trades': active_trades,
        'total_volume': total_volume,
        'volume_in_millions': volume_in_millions,
        'volume_data': volume_data
    })

@staff_member_required
def admin_traders(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_traders.html', {'users': users})

@staff_member_required
def admin_trades(request):
    # Get all trades ordered by creation date (newest first)
    trades = Trade.objects.all().order_by('-created_at')
    return render(request, 'admin_trades.html', {'trades': trades})

@staff_member_required
def admin_wallet(request):
    return render(request, 'admin_wallet.html')

@staff_member_required
def admin_finance(request):
    return render(request, 'admin_finance.html')

@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            # Get the user
            user = User.objects.get(id=user_id)
            
            # Delete the user (this will cascade delete related objects if set up properly)
            user.delete()
            
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def update_trader(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            field = data.get('field')
            value = data.get('value')
            
            # Get the user
            user = User.objects.get(id=user_id)
            
            # Update the appropriate field
            if field == 'name':
                # Split the name into first_name and last_name
                name_parts = value.split(' ', 1)
                user.first_name = name_parts[0]
                user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            elif field == 'email':
                # Validate email format
                from django.core.validators import validate_email
                validate_email(value)
                user.email = value
            elif field == 'username':
                # Check if username is already taken
                if User.objects.filter(username=value).exclude(id=user_id).exists():
                    return JsonResponse({'success': False, 'error': 'Username already taken'})
                user.username = value
            elif field == 'balance':
                # Update user's balance (assuming you have a UserProfile model with balance field)
                try:
                    # Remove currency symbol and convert to float
                    clean_value = value.replace('$', '').strip()
                    balance = float(clean_value)
                    
                    # Update balance in your user profile model
                    profile = user.profile  # Adjust based on your actual model relationship
                    profile.balance = balance
                    profile.save()
                except (ValueError, AttributeError):
                    return JsonResponse({'success': False, 'error': 'Invalid balance format'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid field'})
            
            # Save the user
            user.save()
            
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'error': str(e)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def toggle_user_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            is_active = data.get('is_active')
            
            # Get the user
            user = User.objects.get(id=user_id)
            
            # Update user status
            user.is_active = is_active
            user.save()
            
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def reset_user_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            new_password = data.get('new_password')
            
            if not new_password or len(new_password) < 8:
                return JsonResponse({
                    'success': False, 
                    'error': 'Password must be at least 8 characters long'
                })
            
            # Get the user
            user = User.objects.get(id=user_id)
            
            # Set new password
            user.set_password(new_password)
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Password reset successfully'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': 'User not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False, 
        'error': 'Invalid request method'
    })

@login_required
@require_http_methods(["POST"])
def update_trade(request):
    try:
        data = json.loads(request.body)
        trade_id = data.get('trade_id')
        field = data.get('field')
        value = data.get('value')

        if not trade_id or not field:
            return JsonResponse({
                'success': False,
                'error': 'Trade ID and field are required'
            })

        try:
            # Get the trade
            trade = Trade.objects.get(id=trade_id)
            
            # Update the specified field
            if field == 'symbol':
                trade.symbol = value
            elif field == 'type':
                trade.type = value.lower()
            elif field == 'quantity':
                trade.quantity = Decimal(str(value))
                # Recalculate total amount
                trade.total_amount = trade.quantity * trade.entry_price
            elif field == 'entry_price':
                trade.entry_price = Decimal(str(value))
                # Recalculate total amount
                trade.total_amount = trade.quantity * trade.entry_price
            elif field == 'status':
                trade.status = value.lower()
            
            trade.save()

            # Format the value for display
            formatted_value = value
            if field in ['quantity', 'entry_price']:
                formatted_value = float(getattr(trade, field))
            
            return JsonResponse({
                'success': True,
                'message': 'Trade updated successfully',
                'trade_id': trade.id,
                'field': field,
                'value': formatted_value
            })
        except Trade.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Trade not found'
            })
        except (ValueError, InvalidOperation) as e:
            return JsonResponse({
                'success': False,
                'error': f'Invalid value: {str(e)}'
            })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })






