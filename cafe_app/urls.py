from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<int:category_id>/", views.home, name="category_home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("profile/", views.profile_view, name="profile_view"),
    path("cart/", views.view_cart, name="view_cart"),
    path("about/", views.about_view, name="about_view"),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "update-cart/<str:cart_key>/<str:action>/",
        views.update_cart,
        name="update_cart",
    ),
]
