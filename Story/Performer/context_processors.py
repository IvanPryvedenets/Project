from .models import Basket
from .forms import UserLoginForm


def context_processor(request):

    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.cycle_key

    baskets = Basket.objects.filter(session_key=session_key)

    sum_of_products = 0
    sum_of_price = 0
    sum_of_weight = 0

    for basket in baskets:
        sum_of_products += basket.number
        sum_of_price += basket.total_price
        sum_of_weight += basket.product.weight

    user_login_form = UserLoginForm()

    return {'baskets': baskets, 'sum_of_products': sum_of_products, 'sum_of_price': sum_of_price, 'sum_of_weight': sum_of_weight, 'user_login_form': user_login_form}

