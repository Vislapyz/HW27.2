import stripe

from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создает продукт в Stripe."""
    product_name = f"{product.course}" if product.course else f"{product.lesson}"
    stripe_product = stripe.Product.create(name=f"{product_name}")
    return stripe_product["id"]


def create_stripe_price(product, product_id):
    """Cоздание цены в Stripe."""
    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=product.amount * 100,
        product=product_id
    )
    price_id = stripe_price['id']
    return price_id


def create_stripe_session(price_id):
    """Создание сессии на оплату в Stripe."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
