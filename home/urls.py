from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('product-detail/<slug:slug>',views.product_detail,name="product_detail"),
    path('register-page',views.register_page,name="register_page"),
    path('login-page',views.login_page,name="login_page"),
    path('logout-user',views.logout_user,name="logout_user"),
    path('category-wise',views.category_wise,name="category_wise"),
    path('filter-category',views.filter_category,name="filter_category"),
    path('api/user/validate/<username>/<field>',views.user_validate,name="user_validate"),
    path('cart-page',views.cart_page,name="cart_page"),
    path('cart-minus/<id>',views.cart_minus,name="cart_minus"),
    path('cart-add/<id>',views.cart_add,name="cart_minus"),
    path('cart-remove/<id>',views.cart_remove,name="cart_remove"),
    path('checkout',views.checkout,name="checkout"),
    path('success/',views.payment_success,name="success"),
    path('order-details',views.Orders_page,name="order_page"),
    path('add-comment',views.add_comment,name="add_comment"),

]