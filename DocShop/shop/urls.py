from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from shop import settings
from store.views import index, product_detail, add_to_cart, cart, delete_cart, electronique, product_detail_electronique, add_to_cart_electronique, cart_electronique, delete_cart_electronique, cosmetique, product_detail_cosmetique, add_to_cart_cosmetique, cart_cosmetique, delete_cart_cosmetique, bijoux, cart_bijoux, delete_cart_bijoux, product_detail_bijoux, add_to_cart_bijoux, search, search_electronique, search_cosmetique, search_bijoux, create_checkout_session, create_checkout_session_bijoux, create_checkout_session_cosmetique, create_checkout_session_electronique, accueil, supprimer_order_du_panier,  supprimer_order_du_panier_cosmetique


from accounts.views import signup, logout_user, login_user

from store.views import supprimer_order_du_panier_electronique, supprimer_order_du_panier_bijoux, webhook_handler, payment_callback, create_payment, success
from store.views import profil,cancel

urlpatterns = [
    path('search/', search, name='search'),
    path('profil/', profil, name='profil'),
    path('search_electronique/', search_electronique, name='search_electronique'),
    path('search_cosmetique/', search_cosmetique, name='search_cosmetique'),
    path('search_bijoux/', search_bijoux, name='search_bijoux'),
    path('buy/<slug:product_slug>/', create_checkout_session, name="buy"),
    path('buyb/<slug:Bijoux_slug>/', create_checkout_session_bijoux, name="buyb"),
    path('buyc/<slug:Cosmetique_slug>/', create_checkout_session_cosmetique, name="buyc"),
    path('buye/<slug:Electronique_slug>/', create_checkout_session_electronique, name="buye"),
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel"),
    path('index/', index, name='index'),
    path('', accueil, name='accueil'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('electronique/', electronique, name="electronique"),
    path('cosmetique/', cosmetique, name="cosmetique"),
    path('bijoux/', bijoux, name="bijoux"),
    path('cart/', cart, name="cart"),
    path('cart_electronique/', cart_electronique, name="cart_electronique"),
    path('cart_cosmetique/', cart_cosmetique, name="cart_cosmetique"),
    path('cart_bijoux/', cart_bijoux, name="cart_bijoux"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('cart/delete/<int:order_id>/', supprimer_order_du_panier, name="supprimer_order"),
    path('cart_electronique/delete/<int:order_id>/', supprimer_order_du_panier_electronique, name="supprimer_order_electronique"),
    path('cart_bijoux/delete/<int:order_id>/', supprimer_order_du_panier_bijoux, name="supprimer_order_bijoux"),
    path('cart_cosmetique/delete/<int:order_id>/', supprimer_order_du_panier_cosmetique, name="supprimer_order_cosmetique"),
    path('cart_electronique/delete/', delete_cart_electronique, name="delete-cart-electronique"),
    path('cart_cosmetique/delete/', delete_cart_cosmetique, name="delete-cart-cosmetique"),
    path('cart_bijoux/delete/', delete_cart_bijoux, name="delete-cart-bijoux"),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add-to-cart/', add_to_cart, name="add-to-cart"),
    path('Cosmetique/<str:slug>/', product_detail_cosmetique, name="cosmetique-detail"),
    path('Electronique/<str:slug>/', product_detail_electronique, name="electronique-detail"),
    path('Bijoux/<str:slug>/', product_detail_bijoux, name="bijoux-detail"),
    path('Electronique/<str:slug>/add-to-cart-electronique/', add_to_cart_electronique, name="add-to-cart-electronique"),
    path('Cosmetique/<str:slug>/add-to-cart-cosmetique/', add_to_cart_cosmetique, name="add-to-cart-cosmetique"),
    path('Bijoux/<str:slug>/add-to-cart-bijoux/', add_to_cart_bijoux, name="add-to-cart-bijoux"),
    path('payment/create/', create_payment, name='create_payment'),
    path('payment/callback/', payment_callback, name='payment_callback'),
    path('webhooks/notchpay/', webhook_handler, name='webhook_handler'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
