from django.conf import settings
from mitienda.models import Products
from decimal import Decimal



class Cart:

    def __init__(self,request):
        self.sessions = request.session
        cart = self.session.get(settings.CART_SESSION_id)
        if not cart:
            cart = cart.session[settings.CART_SESSION_id] = {} #Inicializamos en formato json
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0,
                                     'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified=True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        products_id=self.cart.keys()
        products = Products.objects.filter(id__in=products_ids)
        cart = self.cart.copy
        for product in products:
            cart[str(products_ids)]['products'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # Contar los items del carro
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        # Costo total del carrito
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # remover el carro de la sesión
        del self.session[settings.CART_SESSION_ID]
        self.save()