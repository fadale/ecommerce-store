from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

        path("", home, name="home"),
        path("register/", register, name="register"),
        path("login/", login1, name="login"),
        path("my_account/", my_account, name="my_account"),
        path('logout/',logout, name="logout"),
        path("product/<int:pk>", product_Details, name="product_Details"),
        path("products", product_list_api, name="product_list"),
        path("productss", product_list_api, name="product_list_api"),
        path("products/page/<int:page>", product_list_pagination, name="product_list_pagination"),
        path("products-/<int:order_cat>", orderd_product_list, name="orderd_product_list"),
        path("products-/<int:order_cat>/page/<int:page>", orderd_product_list, name="orderd_product_list"),
        path("products/category/<int:category_pk>", product_category, name="product_category"),
        path("products/category/<int:category_pk>/page/<int:page>", product_category, name="product_category"),
        path("products/Prand/<int:prand_pk>", product_prand_list, name="product_prand_list"),
        path("products/Prand/<int:prand_pk>/page/<int:page>", product_prand_list, name="product_prand_list"),
        path("products/tag/<int:tag_pk>", product_tag_list, name="product_tag_list"),
        path("products/tag/<int:tag_pk>/page/<int:page>", product_tag_list, name="product_tag_list"),
        path("products/price/<int:price_cat>", product_list_price, name="product_list_price"),
        path("products/price/<int:price_cat>/page/<int:page>", product_list_price, name="product_list_price"),
        path("products/category/<int:category_pk>/price/<int:price_cat>",
              product_list_priceAndCategory,
                name="product_list_priceAndCategory"),
        path("products/category/<int:category_pk>/prand/<int:prand_pk>",
              product_category_prand_list,
                name="product_category_prand_list"),
        path("products/category/<int:category_pk>/prand/<int:prand_pk>/page/<int:page>",
              product_category_prand_list,
                name="product_category_prand_list"),
        path("products.json",listing_api,name="products-api"),
        path('update_item/', updateItem, name="update_item"),
        path('by_now/<int:pk>', byNowItem ,name="by_now"),
        path("products.json/<int:category_pk>",listing_category_api,name="products-cat-api"),
        path("cart/", cart, name="cart"),
        path("checkout/", checkout, name="checkout"),
        path("delete_cart/<int:pk>",delete_cart,name="delete_cart"),
        path("Logout", Logout, name="Logout"),
        path("contact", contact, name="contact"),
        path("change_password", change_password, name="change_password"),
        path("proccess_order/", proccessOrder, name="proccess_order"),
        path("wishlist/",wishlist,name="wishlist"),
        path("add-to-wishlist",addToWishlist,name="add-to-wishlist")
]
