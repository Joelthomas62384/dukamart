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

]