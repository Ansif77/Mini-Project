
from django.urls import path
from app1 import views


urlpatterns = [
    path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('products/',views.product,name='product'),
    path('addcart/<int:case_id>',views.add_cart,name='addcart'),
    path('viewcart/',views.view_cart,name='viewcart'),
    path('deletecart/<int:case_id>', views.delete_cart, name='deletecart'),
    path('purchase/',views.purchase_view,name='purchase'),
    path('cart/increase/<int:item_id>/', views.increase_qty, name='increase_qty'),
    path('cart/decrease/<int:item_id>/', views.decrease_qty, name='decrease_qty'),
    path('buynow/<int:case_id>',views.purchase_view,name='buynow'),
    path('success/',views.success,name='success'),
    path('cancel/',views.cancel,name='cancel'),
    path('oredered_item/',views.order_view,name='ordered')
]
