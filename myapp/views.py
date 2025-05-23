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
from django.views.decorators.http import require_http_methods, require_POST
from decimal import Decimal, InvalidOperation
import logging
from django.db.models import Count, Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import TruncMonth
from django.core.files.storage import default_storage
import uuid
from .models import Trade, WishlistItem, PaymentMethod, Transaction, Withdrawal
from django.db import models

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
    # Get all approved transactions for the user
    approved_deposits = Transaction.objects.filter(
        user=request.user,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Get all completed withdrawals
    completed_withdrawals = Withdrawal.objects.filter(
        user=request.user,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Get total amount of active trades
    active_trades_total = Trade.objects.filter(
        user=request.user,
        status='active'
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

    # Calculate available balance by subtracting both completed withdrawals and active trades
    available_balance = approved_deposits - completed_withdrawals - active_trades_total

    # Get payment methods
    payment_methods = PaymentMethod.objects.filter(status='active')

    context = {
        'payment_methods': payment_methods,
        'available_balance': available_balance,
        'date_joined': request.user.date_joined.strftime('%d/%m/%Y'),
        'last_login': request.user.last_login.strftime('%d/%m/%Y %I:%M %p')
    }

    return render(request, 'dashboard.html', context)

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
    # Get all active trades for the current user
    trades = Trade.objects.filter(user=request.user, status='active').order_by('-created_at')
    
    # Calculate available balance
    approved_deposits = Transaction.objects.filter(
        user=request.user,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    completed_withdrawals = Withdrawal.objects.filter(
        user=request.user,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    active_trades_total = Trade.objects.filter(
        user=request.user,
        status='active'
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

    available_balance = approved_deposits - completed_withdrawals - active_trades_total
    
    # Calculate floating profit/loss from active trades
    floating_pnl = Decimal('0')
    for trade in trades:
        current_price = get_current_price(trade.symbol)
        if current_price is not None:
            if trade.type == 'BUY':
                pnl = (Decimal(str(current_price)) - trade.entry_price) * trade.quantity
            else:  # SELL
                pnl = (trade.entry_price - Decimal(str(current_price))) * trade.quantity
            floating_pnl += pnl
    
    # Calculate equity (balance + floating P/L)
    equity = available_balance + floating_pnl
    
    context = {
        'trades': trades,
        'available_balance': available_balance,
        'equity': equity,
        'floating_pnl': floating_pnl
    }
    return render(request, 'trades.html', context)

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

        # Convert all numeric values to Decimal
        quantity = Decimal(str(data['quantity']))
        entry_price = Decimal(str(data['price']))
        total_amount = quantity * entry_price

        # Get user's available balance
        approved_deposits = Transaction.objects.filter(
            user=request.user,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        completed_withdrawals = Withdrawal.objects.filter(
            user=request.user,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        # Get total amount of existing active trades
        active_trades_total = Trade.objects.filter(
            user=request.user,
            status='active'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

        # Calculate available balance by subtracting both completed withdrawals and active trades
        available_balance = approved_deposits - completed_withdrawals - active_trades_total

        # Check if user has sufficient funds
        if total_amount > available_balance:
            return JsonResponse({
                'success': False,
                'error': 'Insufficient funds. Please add more funds to your account to complete this trade.',
                'required_amount': float(total_amount),
                'available_balance': float(available_balance)
            })

        # Create new trade
        trade = Trade.objects.create(
            user=request.user,
            symbol=data['symbol'],
            type=data['type'],
            quantity=quantity,
            entry_price=entry_price,
            total_amount=total_amount,
            status='active',
            stop_loss=Decimal(str(data['stopLoss'])) if data['stopLoss'] else None,
            take_profit=Decimal(str(data['takeProfit'])) if data['takeProfit'] else None
        )

        # Calculate new balance after trade
        new_balance = available_balance - total_amount

        return JsonResponse({
            'success': True,
            'message': 'Trade executed successfully',
            'trade_id': trade.id,
            'new_balance': float(new_balance)
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
    pending_transactions = Transaction.objects.filter(status='pending').count()
    
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

    # Get recent trades for the Recent Activity section
    recent_trades = Trade.objects.select_related('user').order_by('-created_at')[:5]

    # Get top traders based on transaction count and total amount
    top_traders = User.objects.annotate(
        transaction_count=Count('transaction', filter=models.Q(transaction__status='completed')),
        total_amount=Sum('transaction__amount', filter=models.Q(transaction__status='completed'))
    ).exclude(total_amount=None).order_by('-total_amount')[:5]

    # Debug prints
    print("Top Traders Query:", top_traders.query)
    print("Top Traders Count:", top_traders.count())
    for trader in top_traders:
        print(f"Trader: {trader.username}, Transactions: {trader.transaction_count}, Total: {trader.total_amount}")

    return render(request, 'admin_dashboard.html', {
        'total_traders': total_traders,
        'active_trades': active_trades,
        'pending_transactions': pending_transactions,
        'total_volume': total_volume,
        'volume_in_millions': volume_in_millions,
        'volume_data': volume_data,
        'recent_trades': recent_trades,
        'top_traders': top_traders
    })

@staff_member_required
def admin_traders(request):
    users = User.objects.all().order_by('-date_joined')
    
    # Calculate balance for each user
    for user in users:
        # Get all approved transactions for the user
        approved_deposits = Transaction.objects.filter(
            user=user,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        # Get all completed withdrawals
        completed_withdrawals = Withdrawal.objects.filter(
            user=user,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        # Get total amount of active trades
        active_trades_total = Trade.objects.filter(
            user=user,
            status='active'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

        # Calculate available balance
        user.available_balance = approved_deposits - completed_withdrawals - active_trades_total
    
    return render(request, 'admin_traders.html', {'users': users})

@staff_member_required
def admin_trades(request):
    # Get all trades ordered by creation date (newest first)
    trades = Trade.objects.all().order_by('-created_at')
    return render(request, 'admin_trades.html', {'trades': trades})

@staff_member_required
def admin_wallet(request):
    payment_methods = PaymentMethod.objects.all().order_by('-created_at')
    context = {
        'payment_methods': payment_methods
    }
    return render(request, 'admin_wallet.html', context)

@csrf_exempt
@staff_member_required
def save_payment_method(request):
    if request.method == 'POST':
        try:
            print("Received payment method request")  # Debug print
            data = json.loads(request.body)
            print("Request data:", data)  # Debug print
            
            payment_type = data.get('payment_type')
            if not payment_type:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Payment type is required'
                }, status=400)
            
            # Create new payment method
            payment_method = PaymentMethod(
                user=request.user,
                payment_type=payment_type,
                status='active'
            )
            
            # Set fields based on payment type
            if payment_type == 'bank':
                payment_method.bank_name = data.get('bank_name')
                payment_method.account_number = data.get('account_number')
                payment_method.ifsc_code = data.get('ifsc_code')
                
                # Validate required fields for bank
                if not all([payment_method.bank_name, payment_method.account_number]):
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Bank name and account number are required'
                    }, status=400)
                    
            elif payment_type == 'card':
                payment_method.card_provider = data.get('card_provider')
                payment_method.api_key = data.get('api_key')
                
                # Validate required fields for card
                if not payment_method.card_provider:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Card provider is required'
                    }, status=400)
                    
            elif payment_type == 'crypto':
                payment_method.wallet_address = data.get('wallet_address')
                
                # Validate required fields for crypto
                if not payment_method.wallet_address:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Wallet address is required'
                    }, status=400)
                    
            elif payment_type == 'paypal':
                payment_method.paypal_email = data.get('paypal_email')
                payment_method.client_id = data.get('client_id')
                
                # Validate required fields for PayPal
                if not payment_method.paypal_email:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'PayPal email is required'
                    }, status=400)
            elif payment_type == 'upi':
                payment_method.upi_id = data.get('upi_id')
                payment_method.account_name = data.get('account_name')
                
                # Validate required fields for UPI
                if not all([payment_method.upi_id, payment_method.account_name]):
                    return JsonResponse({
                        'status': 'error',
                        'message': 'UPI ID and Account Name are required'
                    }, status=400)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid payment type'
                }, status=400)
            
            print("Saving payment method:", payment_method.__dict__)  # Debug print
            payment_method.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Payment method added successfully',
                'payment_method': {
                    'id': payment_method.id,
                    'type': payment_method.get_payment_type_display(),
                    'status': payment_method.status
                }
            })
            
        except json.JSONDecodeError as e:
            print("JSON decode error:", str(e))  # Debug print
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            print("Error saving payment method:", str(e))  # Debug print
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

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
                try:
                    # Remove currency symbol and convert to Decimal
                    clean_value = value.replace('$', '').strip()
                    balance = Decimal(clean_value)
                    
                    # Get current available balance
                    approved_deposits = Transaction.objects.filter(
                        user=user,
                        status='completed'
                    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

                    completed_withdrawals = Withdrawal.objects.filter(
                        user=user,
                        status='completed'
                    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

                    active_trades_total = Trade.objects.filter(
                        user=user,
                        status='active'
                    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

                    current_balance = approved_deposits - completed_withdrawals - active_trades_total
                    
                    # Calculate the difference to adjust
                    adjustment = balance - current_balance
                    
                    # Create a new transaction for the adjustment
                    Transaction.objects.create(
                        user=user,
                        amount=adjustment,
                        status='completed',
                        payment_type='balance_adjustment',
                        transaction_id=f"ADJ-{uuid.uuid4().hex[:8].upper()}"
                    )
                    
                    # Calculate new available balance
                    new_approved_deposits = Transaction.objects.filter(
                        user=user,
                        status='completed'
                    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
                    
                    available_balance = new_approved_deposits - completed_withdrawals - active_trades_total
                    
                    return JsonResponse({
                        'success': True,
                        'available_balance': float(available_balance)
                    })
                    
                except (ValueError, InvalidOperation):
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

@csrf_exempt
def delete_trade(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            trade_id = data.get('trade_id')
            
            # Get the trade
            trade = Trade.objects.get(id=trade_id)
            
            # Delete the trade
            trade.delete()
            
            return JsonResponse({'success': True})
        except Trade.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Trade not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def admin_dashboard_chart_data(request):
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
        volume_data['volumes'].append(round(entry['volume'] / 1000000, 2))  # Convert to millions
        
    return JsonResponse(volume_data)

@require_POST
@csrf_exempt
def toggle_payment_method_status(request, payment_method_id):
    try:
        payment_method = PaymentMethod.objects.get(id=payment_method_id)
        # Toggle the status
        payment_method.status = 'inactive' if payment_method.status == 'active' else 'active'
        payment_method.save()
        return JsonResponse({'status': 'success', 'message': 'Payment method status updated successfully'})
    except PaymentMethod.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Payment method not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_POST
@csrf_exempt
def delete_payment_method(request, payment_method_id):
    try:
        payment_method = PaymentMethod.objects.get(id=payment_method_id)
        payment_method.delete()
        return JsonResponse({'status': 'success', 'message': 'Payment method deleted successfully'})
    except PaymentMethod.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Payment method not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["POST"])
@login_required
def submit_payment_proof(request):
    try:
        # Get form data
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        payment_type = request.POST.get('payment_type')
        receipt_file = request.FILES.get('receipt')
        
        # Convert amount to Decimal
        try:
            amount = Decimal(str(amount))
        except (TypeError, ValueError, InvalidOperation):
            return JsonResponse({
                'success': False,
                'message': 'Invalid amount value'
            }, status=400)
        
        # Get transaction reference based on payment type
        transaction_ref = None
        if payment_type == 'bank':
            transaction_ref = request.POST.get('transaction_ref')
        elif payment_type == 'crypto':
            transaction_ref = request.POST.get('transaction_hash')
        elif payment_type in ['paypal', 'upi']:
            transaction_ref = request.POST.get('transaction_id')

        if not transaction_ref:
            return JsonResponse({
                'success': False,
                'message': 'Transaction reference is required'
            }, status=400)

        # Generate unique transaction ID
        transaction_id = f"TRX-{uuid.uuid4().hex[:8].upper()}"

        # Create transaction record
        transaction = Transaction.objects.create(
            transaction_id=transaction_id,
            user=request.user,
            payment_type=payment_type,
            amount=amount,
            currency=currency,
            transaction_reference=transaction_ref,
            receipt_file=receipt_file if receipt_file else None,
            status='pending'  # Set initial status as pending
        )

        return JsonResponse({
            'success': True,
            'message': 'Payment proof submitted successfully',
            'transaction_id': transaction_id,
            'transaction_reference': transaction_ref  # Include in response
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@require_http_methods(["GET"])
@login_required
def get_transactions(request):
    try:
        # Get all transactions
        transactions = Transaction.objects.all().order_by('-created_at')  # Order by newest first
        
        # Convert to list of dictionaries
        transaction_list = []
        for transaction in transactions:
            transaction_list.append({
                'transaction_id': transaction.transaction_id,
                'user_name': transaction.user.username,
                'payment_type': transaction.get_payment_type_display(),
                'amount': float(transaction.amount),
                'currency': transaction.currency,
                'status': transaction.status,
                'created_at': transaction.created_at.isoformat(),
                'receipt_url': transaction.receipt_file.url if transaction.receipt_file else None,
                'transaction_reference': transaction.transaction_reference or 'N/A'  # Ensure we always have a value
            })

        return JsonResponse({
            'success': True,
            'transactions': transaction_list
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@require_http_methods(["GET"])
@login_required
def transaction_details(request, transaction_id):
    try:
        # Get transaction details
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        
        return JsonResponse({
            'success': True,
            'transaction_id': transaction.transaction_id,
            'user_name': transaction.user.username,
            'payment_type': transaction.get_payment_type_display(),
            'amount': float(transaction.amount),
            'currency': transaction.currency,
            'status': transaction.status,
            'created_at': transaction.created_at.isoformat(),
            'receipt_url': transaction.receipt_file.url if transaction.receipt_file else None,
            'transaction_reference': transaction.transaction_reference
        })

    except Transaction.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Transaction not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
def update_transaction_status(request, transaction_id):
    if request.method == 'POST':
        try:
            # Get the transaction
            transaction = Transaction.objects.get(transaction_id=transaction_id)
            
            # Get the new status from request body
            data = json.loads(request.body)
            new_status = data.get('status')
            
            # Map 'approved' to 'completed' for backward compatibility
            if new_status == 'approved':
                new_status = 'completed'
            
            # Validate status
            if new_status not in ['pending', 'completed', 'failed']:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid status value'
                }, status=400)
            
            # Update the status
            transaction.status = new_status
            transaction.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Transaction status updated successfully'
            })
            
        except Transaction.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Transaction not found'
            }, status=404)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)

@login_required
@require_POST
def submit_withdrawal(request):
    try:
        # Get form data
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        bank_name = request.POST.get('bankName')
        account_number = request.POST.get('accountNumber')
        account_holder = request.POST.get('accountHolder')
        ifsc_code = request.POST.get('ifscCode')

        # Validate amount
        try:
            amount = float(amount)
            if amount < 10:
                return JsonResponse({
                    'success': False,
                    'message': 'Minimum withdrawal amount is $10'
                })
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid amount'
            })

        # Generate unique transaction ID
        transaction_id = f"WD-{uuid.uuid4().hex[:8].upper()}"

        # Create withdrawal record
        withdrawal = Withdrawal.objects.create(
            user=request.user,
            amount=amount,
            currency=currency,
            bank_name=bank_name,
            account_number=account_number,
            account_holder=account_holder,
            ifsc_code=ifsc_code,
            transaction_id=transaction_id
        )

        return JsonResponse({
            'success': True,
            'message': 'Withdrawal request submitted successfully',
            'transaction_id': transaction_id
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@require_http_methods(["GET"])
@login_required
def get_withdrawals(request):
    try:
        # Get all withdrawals ordered by creation date (newest first)
        withdrawals = Withdrawal.objects.all().order_by('-created_at')
        
        # Format the data for the frontend
        withdrawals_data = []
        for withdrawal in withdrawals:
            # Format bank details
            bank_details = None
            if withdrawal.bank_name or withdrawal.account_number:
                bank_details = {
                    'bank_name': withdrawal.bank_name or 'Not Provided',
                    'account_number': withdrawal.account_number or 'Not Provided',
                    'account_holder': withdrawal.account_holder or 'Not Provided',
                    'ifsc_code': withdrawal.ifsc_code or 'Not Provided'
                }

            # Format amount with currency
            formatted_amount = f"{withdrawal.amount} {withdrawal.currency}"

            # Determine payment method based on available fields
            payment_method = None
            if withdrawal.payment_method:
                payment_method = withdrawal.get_payment_method_display()
            elif withdrawal.bank_name:
                payment_method = "Bank Transfer"
            elif withdrawal.wallet_address:
                payment_method = "Cryptocurrency"
            elif withdrawal.paypal_email:
                payment_method = "PayPal"
            elif withdrawal.upi_id:
                payment_method = "UPI"
            else:
                payment_method = "Bank Transfer"  # Default to Bank Transfer if no specific method is found

            # Format date
            formatted_date = withdrawal.created_at.strftime("%B %d, %Y %H:%M")

            withdrawals_data.append({
                'withdrawal_id': withdrawal.id,
                'user_name': withdrawal.user.username,
                'currency': withdrawal.currency,
                'amount': str(withdrawal.amount),
                'formatted_amount': formatted_amount,
                'payment_method': payment_method,
                'status': withdrawal.status,
                'created_at': formatted_date,
                'proof_url': withdrawal.proof.url if withdrawal.proof else None,
                'bank_details': bank_details,
                'transaction_id': withdrawal.transaction_id or 'Not Available',
                'notes': withdrawal.notes or 'No additional notes'
            })
        
        return JsonResponse({
            'status': 'success',
            'withdrawals': withdrawals_data
        })
    except Exception as e:
        print(f"Error fetching withdrawals: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to fetch withdrawals'
        }, status=500)

@require_http_methods(["GET"])
@login_required
def withdrawal_details(request, withdrawal_id):
    try:
        withdrawal = Withdrawal.objects.get(id=withdrawal_id)
        
        # Format bank details if available
        bank_details = None
        if withdrawal.bank_name or withdrawal.account_number:
            bank_details = {
                'bank_name': withdrawal.bank_name or 'Not Provided',
                'account_number': withdrawal.account_number or 'Not Provided',
                'account_holder': withdrawal.account_holder or 'Not Provided',
                'ifsc_code': withdrawal.ifsc_code or 'Not Provided'
            }
        
        # Format amount with currency
        formatted_amount = f"{withdrawal.amount} {withdrawal.currency}"
        
        # Format payment method
        payment_method = withdrawal.get_payment_method_display() if withdrawal.payment_method else "Not Specified"
        
        # Format date
        formatted_date = withdrawal.created_at.strftime("%B %d, %Y %H:%M")
        
        return JsonResponse({
            'status': 'success',
            'withdrawal_id': withdrawal.id,
            'user_name': withdrawal.user.username,
            'currency': withdrawal.currency,
            'amount': str(withdrawal.amount),
            'formatted_amount': formatted_amount,
            'payment_method': payment_method,
            'status': withdrawal.status,
            'created_at': formatted_date,
            'proof_url': withdrawal.proof.url if withdrawal.proof else None,
            'bank_details': bank_details,
            'transaction_id': withdrawal.transaction_id or 'Not Available',
            'notes': withdrawal.notes or 'No additional notes'
        })
    except Withdrawal.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Withdrawal not found'
        }, status=404)
    except Exception as e:
        print(f"Error fetching withdrawal details: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to fetch withdrawal details'
        }, status=500)

@require_http_methods(["POST"])
@login_required
def update_withdrawal_status(request, withdrawal_id):
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if not new_status or new_status not in ['pending', 'completed', 'failed']:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid status'
            }, status=400)
        
        withdrawal = Withdrawal.objects.get(id=withdrawal_id)
        withdrawal.status = new_status
        withdrawal.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Withdrawal status updated successfully'
        })
    except Withdrawal.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Withdrawal not found'
        }, status=404)
    except Exception as e:
        print(f"Error updating withdrawal status: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to update withdrawal status'
        }, status=500)

@csrf_exempt
@staff_member_required
def login_as_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            if not user_id:
                return JsonResponse({
                    'success': False,
                    'error': 'User ID is required'
                })
            
            # Get the target user
            try:
                target_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'User not found'
                })
            
            # Log out the current admin user
            logout(request)
            
            # Log in as the target user
            login(request, target_user)
            
            return JsonResponse({
                'success': True,
                'redirect_url': '/dashboard/'
            })
            
        except Exception as e:
            print(f"Error in login_as_user: {e}")
            return JsonResponse({
                'success': False,
                'error': 'Failed to login as user'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })





