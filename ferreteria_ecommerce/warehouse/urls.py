from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    path('order/<str:order_number>/', views.order_detail_warehouse, name='order_detail'),
    path('confirm/<str:order_number>/', views.confirm_order, name='confirm_order'),
    path('ship/<str:order_number>/', views.ship_order, name='ship_order'),
    path('ready-to-ship/<str:order_number>/', views.mark_ready_to_ship, name='mark_ready_to_ship'),
    path('delivered/<str:order_number>/', views.mark_delivered, name='mark_delivered'),
    path('delete-all-orders/', views.delete_all_orders, name='delete_all_orders'),
    path('inventory/', views.inventory_movements, name='inventory_movements'),
    path('shipments/', views.shipments_list, name='shipments_list'),
]
