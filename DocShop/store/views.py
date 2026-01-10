from datetime import time
from functools import total_ordering

import stripe.error
from django.conf import settings
from django.contrib.admin.templatetags.admin_list import results
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.urls import reverse
from store.models import product, Cart, Order, Electronique, Cart_electronique, Order_electronique, Cosmetique, Cart_cosmetique, Order_cosmetique, Bijoux, Cart_bijoux, Order_bijoux, Payment, Subscriber
from stripe.api_resources.climate import order
from shop.forms import SubscriptionForm
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import json
import hmac
import hashlib

from shop.settings import NOTCHPAY_API_KEY


# Create your views here.
def index(request):

    products = product.objects.all()
    return render(request, 'index.html', context={"products": products})
def accueil(request):

    return render(request, 'accueil.html')

def product_detail(request, slug):
    productt =get_object_or_404(product, slug=slug)
    return render(request, 'detail.html', context={"product": productt})

def product_detail_electronique(request, slug):
    electronique =get_object_or_404(Electronique, slug=slug)
    return render(request, 'detail_electronique.html', context={"Electronique": electronique})

def product_detail_cosmetique(request, slug):
    cosmetique =get_object_or_404(Cosmetique, slug=slug)
    return render(request, 'detail_cosmetique.html', context={"Cosmetique": cosmetique})

def product_detail_bijoux(request, slug):
    bijoux =get_object_or_404(Bijoux, slug=slug)
    return render(request, 'detail_bijoux.html', context={"Bijoux": bijoux})

def add_to_cart_electronique(request, slug):
    user = request.user
    productt = get_object_or_404(Electronique, slug=slug)
    cart, _ = Cart_electronique.objects.get_or_create(user=user)
    order, created = Order_electronique.objects.get_or_create(user=user,
                                                  ordered=False,
                                                  Electronique=productt)
    if created:
        cart.orders.add(order)
        cart.save()
        productt.stock -= 1
        productt.save()
    else:
        order.quantity += 1
        order.save()
        productt.stock -= 1
        productt.save()

    return redirect(reverse("electronique-detail", kwargs={"slug": slug}))

def add_to_cart_cosmetique(request, slug):
    user = request.user
    productt = get_object_or_404(Cosmetique, slug=slug)
    cart, _ = Cart_cosmetique.objects.get_or_create(user=user)
    order, created = Order_cosmetique.objects.get_or_create(user=user,
                                                  ordered=False,
                                                  Cosmetique=productt)
    if created:
        cart.orders.add(order)
        cart.save()
        productt.stock -= 1
        productt.save()
    else:
        order.quantity += 1
        order.save()
        productt.stock -= 1
        productt.save()

    return redirect(reverse("cosmetique-detail", kwargs={"slug": slug}))

def add_to_cart_bijoux(request, slug):
    user = request.user
    productt = get_object_or_404(Bijoux, slug=slug)
    cart, _ = Cart_bijoux.objects.get_or_create(user=user)
    order, created = Order_bijoux.objects.get_or_create(user=user,
                                                  ordered=False,
                                                  Bijoux=productt)
    if created:
        cart.orders.add(order)
        cart.save()
        productt.stock -= 1
        productt.save()
    else:
        order.quantity += 1
        order.save()
        productt.stock -= 1
        productt.save()

    return redirect(reverse("bijoux-detail", kwargs={"slug": slug}))

def add_to_cart(request, slug):
    user = request.user
    productt = get_object_or_404(product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user,
                                                  ordered=False,
                                                  product=productt)
    if created:
        cart.orders.add(order)
        cart.save()
        productt.stock -= 1
        productt.save()
    else:
        order.quantity += 1
        order.save()
        productt.stock -= 1
        productt.save()

    return redirect(reverse("product", kwargs={"slug": slug}))

def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'cart.html', context={"orders": cart.orders.all()})

def cart_electronique(request):
    cart = get_object_or_404(Cart_electronique, user=request.user)
    return render(request, 'cart_electronique.html', context={"orders": cart.orders.all()})

def cart_cosmetique(request):
    cart = get_object_or_404(Cart_cosmetique, user=request.user)
    return render(request, 'cart_cosmetique.html', context={"orders": cart.orders.all()})

def cart_bijoux(request):
    cart = get_object_or_404(Cart_bijoux, user=request.user)
    return render(request, 'cart_bijoux.html', context={"orders": cart.orders.all()})

def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()

    return redirect('index')

def supprimer_order_du_panier(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, ordered=False)
    order.delete()
    return redirect('cart')

def supprimer_order_du_panier_electronique(request, order_id):
    order = get_object_or_404(Order_electronique, id=order_id, user=request.user, ordered=False)
    order.delete()
    return redirect('cart_electronique')

def supprimer_order_du_panier_bijoux(request, order_id):
    order = get_object_or_404(Order_bijoux, id=order_id, user=request.user, ordered=False)
    order.delete()
    return redirect('cart_bijoux')

def supprimer_order_du_panier_cosmetique(request, order_id):
    order = get_object_or_404(Order_cosmetique, id=order_id, user=request.user, ordered=False)
    order.delete()
    return redirect('cart_cosmetique')

def delete_cart_electronique(request):
    if cart_electronique := request.user.cart_electronique:
        cart_electronique.delete()

    return redirect('electronique')

def delete_cart_cosmetique(request):
    if cart_cosmetique := request.user.cart_cosmetique:
        cart_cosmetique.delete()

    return redirect('cosmetique')

def delete_cart_bijoux(request):
    if cart_bijoux := request.user.cart_bijoux:
        cart_bijoux.delete()

    return redirect('bijoux')

def electronique(request):
    electronique = Electronique.objects.all()
    return render(request, 'electronique.html', context={"electronique": electronique})

def cosmetique(request):
    cosmetique = Cosmetique.objects.all()
    return render(request, 'cosmetique.html', context={"cosmetiques": cosmetique})

def bijoux(request):
    bijoux = Bijoux.objects.all()
    return render(request, 'bijoux.html', context={"bijoux": bijoux})


def search(request):
    query = request.GET.get('q')
    if query:
        results = product.objects.filter(name__icontains=query)
    else:
        results = product.objects.none()
    return render(request, 'search_results.html', {'results': results})

def search_electronique(request):
    query = request.GET.get('qu')
    if query:
        results = Electronique.objects.filter(name__icontains=query)
    else:
        results = Electronique.objects.none()
    return render(request, 'search_results_electronique.html', {'results': results})

def search_cosmetique(request):
    query = request.GET.get('q')
    if query:
        results = Cosmetique.objects.filter(name__icontains=query)
    else:
        results = Cosmetique.objects.none()
    return render(request, 'search_results_cosmetique.html', {'results': results})

def search_bijoux(request):
    query = request.GET.get('q')
    if query:
        results = Bijoux.objects.filter(name__icontains=query)
    else:
        results = Bijoux.objects.none()
    return render(request, 'search_results_bijoux.html', {'results': results})


stripe.api_key = settings.STRIPE_SECRET_KEY
def create_checkout_session(request, product_slug):
    productt = product.objects.get(slug=product_slug)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    else:
        quantity = 1
    unit_price = int(productt.price)  # Convertir en centimes pour Stripe
    total_amount = unit_price * quantity  # Calculer le montant total (en centimes)
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "xaf",
                    "product_data": {
                        "name": productt.name,
                        "images": [request.build_absolute_uri(productt.thumbnail.url)],
                    },
                    "unit_amount": unit_price,  # Prix unitaire en centimes
                },
                "quantity": quantity,  # Quantité saisie
            }],
            mode="payment",
            success_url=request.build_absolute_uri("/success/"),
            cancel_url=request.build_absolute_uri("/cancel/"),
        )
        print("Session Stripe créée avec ID:", checkout_session.id)  # Débogage
        print("URL de redirection Stripe:", checkout_session.url)  # Débogage
        print(f"Quantité: {quantity}, Prix unitaire: {productt.price} XAF, Montant total: {total_amount / 100} XAF")  # Débogage
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print("Erreur lors de la création de la session Stripe:", str(e))  # Débogage
        return HttpResponse(f"Une erreur est survenue : {str(e)}")


def create_checkout_session_bijoux(request, Bijoux_slug):
    bijoux = Bijoux.objects.get(slug=Bijoux_slug)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    else:
        quantity = 1

    try:
        checkout_session_bijoux = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "xaf",
                    "product_data": {
                        "name": bijoux.name,
                        "images": [request.build_absolute_uri(bijoux.thumbnail.url)],
                    },
                    "unit_amount": int(bijoux.price),  # Prix unitaire en centimes
                },
                "quantity": quantity,  # Quantité saisie
            }],
            mode="payment",
            success_url=request.build_absolute_uri("/success/"),
            cancel_url=request.build_absolute_uri("/cancel/"),
        )
        print("Session Stripe créée avec ID:", checkout_session_bijoux.id)  # Débogage
        print("URL de redirection Stripe:", checkout_session_bijoux.url)  # Débogage
        return redirect(checkout_session_bijoux.url, code=303)
    except Exception as e:
        print("Erreur lors de la création de la session Stripe:", str(e))  # Débogage
        return HttpResponse(f"Une erreur est survenue : {str(e)}")


def create_checkout_session_cosmetique(request, Cosmetique_slug):
    cosmetique = Cosmetique.objects.get(slug=Cosmetique_slug)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    else:
        quantity = 1
    unit_price = int(cosmetique.price)  # Convertir en centimes pour Stripe
    total_amount = unit_price * quantity  # Calculer le montant total (en centimes)
    try:
        checkout_session_cosmetique = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "xaf",
                    "product_data": {
                        "name": cosmetique.name,
                        "images": [request.build_absolute_uri(cosmetique.thumbnail.url)],
                    },
                    "unit_amount": unit_price,  # Prix unitaire en centimes
                },
                "quantity": quantity,  # Quantité saisie
            }],
            mode="payment",
            success_url=request.build_absolute_uri("/success/"),
            cancel_url=request.build_absolute_uri("/cancel/"),
        )
        print("Session Stripe créée avec ID:", checkout_session_cosmetique.id)  # Débogage
        print("URL de redirection Stripe:", checkout_session_cosmetique.url)  # Débogage
        print(f"Quantité: {quantity}, Prix unitaire: {cosmetique.price} XAF, Montant total: {total_amount / 100} XAF")  # Débogage
        return redirect(checkout_session_cosmetique.url, code=303)
    except Exception as e:
        print("Erreur lors de la création de la session Stripe:", str(e))  # Débogage
        return HttpResponse(f"Une erreur est survenue : {str(e)}")

def create_checkout_session_electronique(request, Electronique_slug):
    electronique = Electronique.objects.get(slug=Electronique_slug)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    else:
        quantity = 1
    unit_price = int(electronique.price)  # Convertir en centimes pour Stripe
    total_amount = unit_price * quantity  # Calculer le montant total (en centimes)
    try:
        checkout_session_electronique = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "xaf",
                    "product_data": {
                        "name": electronique.name,
                        "images": [request.build_absolute_uri(electronique.thumbnail.url)],
                    },
                    "unit_amount": unit_price,  # Prix unitaire en centimes
                },
                "quantity": quantity,  # Quantité saisie
            }],
            mode="payment",
            success_url=request.build_absolute_uri("/success/"),
            cancel_url=request.build_absolute_uri("/cancel/"),
        )
        print("Session Stripe créée avec ID:", checkout_session_electronique.id)  # Débogage
        print("URL de redirection Stripe:", checkout_session_electronique.url)  # Débogage
        print(f"Quantité: {quantity}, Prix unitaire: {electronique.price} XAF, Montant total: {total_amount / 100} XAF")  # Débogage
        return redirect(checkout_session_electronique.url, code=303)
    except Exception as e:
        print("Erreur lors de la création de la session Stripe:", str(e))  # Débogage
        return HttpResponse(f"Une erreur est survenue : {str(e)}")

def success(request):
    return render(request, "success.html")

def cancel(request):
    return render(request, "cancel.html")


def subcribe(request):
    if request.method == 'POST':
        email = request.POST("email")
        subscribed_on = request.POST("subscribed_on")
        subscriber = Subscriber.objects.create(email=email,
                                               subscribed_on=subscribed_on)
        Subscriber(request, subscriber)
        return redirect('index')

    return render(request, 'index.htmml')


def send_newsletter():
    subscribers = Subscriber.objects.all()
    for subscriber in subscribers:
        send_mail(
            'Notre derniere newsletter',
            'Voici les nouveaux produits ajoute',
            'laboutiquekaj@gmail.com',
            [subscriber.email],
            fail_silently=False,
        )


# Initialize the SDK
notchpay = NOTCHPAY_API_KEY


def create_payment(request):
    if request.method == 'POST':
        try:
            amount = int(request.POST.get('amount', 0))
            email = request.POST.get('email', '')
            name = request.POST.get('name', '')

            if amount < 100 or not email:
                return render(request, 'payment_form.html', {
                    'error': 'Invalid amount or email'
                })

            payment = notchpay.payments.create({
                'amount': amount,
                'currency': 'XAF',
                'customer': {
                    'email': email,
                    'name': name
                },
                'reference': f"django_order_{int(time.time())}",
                'callback': request.build_absolute_uri('/payment/callback/'),
                'description': 'Payment from Django app'
            })

            # Redirect to the payment page
            return redirect(payment.authorization_url)
        except Exception as e:
            return render(request, 'payment_form.html', {
                'error': str(e)
            })

    return render(request, 'payment_form.html')


def payment_callback(request):
    reference = request.GET.get('reference', '')

    if not reference:
        return render(request, 'payment_error.html', {
            'error': 'No reference provided'
        })

    try:
        payment = notchpay.payments.retrieve(reference)

        if payment.transaction.status == 'complete':
            # Payment is complete, fulfill the order
            return render(request, 'payment_success.html', {
                'payment': payment.transaction
            })
        else:
            # Payment is not complete
            return render(request, 'payment_failed.html', {
                'payment': payment.transaction
            })
    except Exception as e:
        return render(request, 'payment_error.html', {
            'error': str(e)
        })


def verify_webhook_signature(payload, signature, secret):
    computed_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)


@csrf_exempt
@require_POST
def webhook_handler(request):
    payload = request.body.decode('utf-8')
    signature = request.headers.get('X-Notchpay-Signature', '')

    if not verify_webhook_signature(payload, signature, settings.NOTCHPAY_WEBHOOK_SECRET):
        return JsonResponse({'error': 'Invalid signature'}, status=401)

    event = json.loads(payload)

    # Process the event based on its type
    event_type = event.get('type', '')

    if event_type == 'payment.complete':
        # Handle completed payment
        payment = event.get('data', {})
        # Update order status, send confirmation email, etc.
        print(f"Payment {payment.get('reference')} completed")
    elif event_type == 'payment.failed':
        # Handle failed payment
        payment = event.get('data', {})
        # Update order status, notify customer, etc.
        print(f"Payment {payment.get('reference')} failed")
    # Handle other event types...

    return JsonResponse({'status': 'success'})

def profil(request):
    return render(request, 'profil.html')


