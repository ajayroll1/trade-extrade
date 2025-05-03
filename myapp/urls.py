from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),  # Made login the root URL
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('trades/', views.trades, name='trades'),
    path('analytics/', views.analytics, name='analytics'),
    path('signal/', views.signal, name='signal'),
    path('pamm/', views.pamm, name='pamm'),
    path('history/', views.history, name='history'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('send-reset-code/', views.send_reset_code, name='send-reset-code'),
    path('verify-reset-code/', views.verify_reset_code, name='verify-reset-code'),
    path('update-password/', views.update_password, name='update-password'),
    path('api/execute_trade/', views.execute_trade, name='execute_trade'),
    path('api/close_trade/', views.close_trade, name='close_trade'),
    path('api/get_live_profit/', views.get_live_profit, name='get_live_profit'),
    path('api/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('api/remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('api/update_wishlist_price/', views.update_wishlist_price, name='update_wishlist_price'),
    path('api/update_trade_status/', views.update_trade_status, name='update_trade_status'),
    path('api/update_sltp/', views.update_sltp, name='update_sltp'),
    path('remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-traders/', views.admin_traders, name='admin_traders'),
    path('admin-trades/', views.admin_trades, name='admin_trades'),
    path('admin-wallet/', views.admin_wallet, name='admin_wallet'),
    path('admin-finance/', views.admin_finance, name='admin_finance'),
    path('api/delete_user/', views.delete_user, name='delete_user'),
    path('api/update_trader/', views.update_trader, name='update_trader'),
    path('api/toggle_user_status/', views.toggle_user_status, name='toggle_user_status'),
    path('api/reset_user_password/', views.reset_user_password, name='reset_user_password'),
    path('api/update_trade/', views.update_trade, name='update_trade'),
    path('api/delete_trade/', views.delete_trade, name='delete_trade'),
]














