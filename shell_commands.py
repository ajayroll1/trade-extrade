from django.contrib.auth.models import User
from myapp.models import Trade, TradeHistory
from decimal import Decimal
from datetime import datetime

# Get first user (या specific user ID use करें)
user = User.objects.first()

# Create a BTC/USDT trade
trade = Trade.objects.create(
    user=user,
    symbol='BTCUSDT',
    type='BUY',
    quantity=Decimal('0.05'),  # 0.05 BTC
    entry_price=Decimal('43250.75'),  # Current BTC price around $43,250
    total_amount=Decimal('2162.53'),  # 0.05 * 43250.75
    status='closed',
    stop_loss=Decimal('42000.00'),
    take_profit=Decimal('45000.00'),
    profit=Decimal('25.50'),  # Example profit
    commission=Decimal('2.16')  # Usually 0.1% of total amount
)

# Add to trade history
trade_history = TradeHistory.objects.create(
    user=user,
    trade_id=trade.id,
    symbol='BTCUSDT',
    type='BUY',
    lot=Decimal('0.05'),
    status='closed',
    entry=Decimal('43250.75'),
    exit=Decimal('43760.75'),  # Exit price higher than entry for profit
    sl=Decimal('42000.00'),
    tp=Decimal('45000.00'),
    commission=Decimal('2.16'),
    profit=Decimal('25.50'),
    swap=Decimal('0.00')
)

# Verify the created trade
print("\nCreated Trade Details:")
print(f"""
Trade ID: {trade.id}
Symbol: {trade.symbol}
Type: {trade.type}
Quantity: {trade.quantity} BTC
Entry Price: ${trade.entry_price:,.2f}
Total Amount: ${trade.total_amount:,.2f}
Status: {trade.status}
Profit: ${trade.profit:,.2f}
Commission: ${trade.commission:,.2f}
Created At: {trade.created_at}
""")

# Verify the trade history
print("\nTrade History Details:")
print(f"""
History ID: {trade_history.id}
Trade ID: {trade_history.trade_id}
Symbol: {trade_history.symbol}
Type: {trade_history.type}
Lot Size: {trade_history.lot} BTC
Entry: ${trade_history.entry:,.2f}
Exit: ${trade_history.exit:,.2f}
Stop Loss: ${trade_history.sl:,.2f}
Take Profit: ${trade_history.tp:,.2f}
Profit: ${trade_history.profit:,.2f}
Commission: ${trade_history.commission:,.2f}
""")