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
]






