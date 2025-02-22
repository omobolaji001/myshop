from .cart import Cart


def cart(request):
    """ Returns the current cart """
    return {'cart': Cart(request)}
