from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cart", views.wishlist, name="cart"),
    path("deactivate",views.deactivate,  name="deactivate"),
    path("addcomment", views.addcomment, name="addcomment"),
    path("remove", views.removefromcart, name="remove"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:id>", views.desc, name="desc"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("category", views.category, name="category"),
    path("<str:category>", views.category_desc, name="categorydesc"),
]
