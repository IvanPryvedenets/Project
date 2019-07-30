from django.views import View
from django.shortcuts import render, redirect
from django.contrib.postgres.search import SearchVector
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .forms import *
from .models import *


# Головна сторінка
class HomePage(View):

    def get(self, request):

        session_key = request.session.session_key
        print(session_key)
        if session_key is None:
            session_key = request.session.cycle_key()

        print(session_key)

        search_query = request.GET.get('search_input', '')

        # Annotate - виконує пошук полів
        if search_query:
            products = Product.objects.annotate(search=SearchVector('title') +
                                                       SearchVector('description') +
                                                       SearchVector('brand') +
                                                       SearchVector('category__field'),).filter(search=search_query)

            return render(request, 'Performer/Search_results.html', context={'products': products})
        else:
            products = Product.objects.all()
            return render(request, 'Performer/Home_page.html', context={'products': products})


# Сторінка з інфою продукту
class ProductInformation(View):

    def get(self, request, slug):

        product = Product.objects.get(slug=slug)

        if request.user.is_authenticated:
            field_data = {
                'user_name': request.user.first_name,
                'user_email': request.user.email,
            }
            form = CommentForm(field_data)
        else:
            form = CommentForm()

        comments = Comment.objects.filter(product=product)
        return render(request, 'Performer/Product_information.html', context={'product': product, 'form': form, 'comments': comments})

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = product
                comment.user_name = form.cleaned_data['user_name']
                comment.user_email = form.cleaned_data['user_email']
                comment.message = form.cleaned_data['message']
                comment.save()
                return redirect(product)
        else:
            form = CommentForm()
            comments = Comment.objects.filter(product=product)
            return render(request, 'Performer/Product_information.html', context={'product': product, 'form': form, 'comments': comments})


# Сторінка корзини
class Cart(View):
    def get(self, request):

        session_key = request.session.session_key

        product_baskets = Basket.objects.filter(session_key=session_key)

        return render(request, 'Performer/Cart.html', context={'product_baskets': product_baskets})


# Сторінка замовлення
class Checkout(View):
    def get(self, request):

        session_key = request.session.session_key

        if request.user.is_authenticated:
            field_data = {
                'buyer_name': request.user.first_name,
                'buyer_lastname': request.user.last_name,
                'buyer_tel': request.user.username,
                'buyer_email': request.user.email,

            }
            form = OrderForm(field_data)
        else:
            form = OrderForm()

        password_form = PasswordForm()

        product_baskets = Basket.objects.filter(session_key=session_key)

        # якщо квірі порожній
        try:
            product_baskets[0]
        except IndexError:
            return redirect('/cart/')

        return render(request, 'Performer/Checkout.html', context={'form': form, 'product_baskets': product_baskets, 'password_form': password_form})

    def post(self, request):

        if request.method == 'POST':

            session_key = request.session.session_key
            form = OrderForm(request.POST)

            # Створення екземпляру замовлення
            if form.is_valid():
                order_form = form.save(commit=False)

                # Якщо юзер зареєстрований, порівняй його поля з прихідними даними
                if request.user.is_authenticated:
                    # Перевір чи збігаються дані з активним узером і відправними даними
                    if request.user.email == request.POST.get('buyer_email') and request.user.username == request.POST.get('buyer_tel'):
                        print('порівняв')
                        pass
                    else:
                        field_data = {
                            'buyer_name': request.user.first_name,
                            'buyer_lastname': request.user.last_name,
                            'buyer_tel': request.user.username,
                            'buyer_email': request.user.email,

                        }
                        form = OrderForm(field_data)

                        password_form = PasswordForm()

                        product_baskets = Basket.objects.filter(session_key=session_key)
                        error = 'Вказано не правильний Email або номер'
                        return render(request, 'Performer/Checkout.html', context={'form': form, 'product_baskets': product_baskets, 'password_form': password_form, 'error': error})
                # Якщо юзер не автентифікований
                else:
                    print('Перевіряю інших юзерів')
                    # Перевір чи є користувач з такою поштою
                    try:
                        user = User.objects.get(email=form.cleaned_data['buyer_email'])

                        if request.user.is_authenticated:
                            field_data = {
                                'buyer_name': request.user.first_name,
                                'buyer_lastname': request.user.last_name,
                                'buyer_tel': request.user.username,
                                'buyer_email': request.user.email,

                            }
                            form = OrderForm(field_data)
                        else:
                            form = OrderForm()

                        password_form = PasswordForm()

                        product_baskets = Basket.objects.filter(session_key=session_key)

                        if user:

                            email_error = 'Такий Email використовується'
                            return render(request, 'Performer/Checkout.html', context={'form': form, 'product_baskets': product_baskets, 'password_form': password_form, 'email_error': email_error})

                    except ObjectDoesNotExist:
                        pass

                    # Перевір чи є користувач з таким емайлом
                    try:
                        user = User.objects.get(username=form.cleaned_data['buyer_tel'])

                        if request.user.is_authenticated:
                            field_data = {
                                'buyer_name': request.user.first_name,
                                'buyer_lastname': request.user.last_name,
                                'buyer_tel': request.user.username,
                                'buyer_email': request.user.email,

                            }
                            form = OrderForm(field_data)
                        else:
                            form = OrderForm()

                        password_form = PasswordForm()

                        product_baskets = Basket.objects.filter(session_key=session_key)

                        if user:

                            tel_error = 'Такий номер використовується'
                            return render(request, 'Performer/Checkout.html', context={'form': form, 'product_baskets': product_baskets, 'password_form': password_form, 'tel_error': tel_error})

                    except ObjectDoesNotExist:
                        pass

                # Якщо приходить поле з паролем
                if request.POST.get('password_2'):

                    user = User.objects.create_user(
                        username=form.cleaned_data['buyer_tel'],
                        first_name=form.cleaned_data['buyer_name'],
                        last_name=form.cleaned_data['buyer_lastname'],
                        email=form.cleaned_data['buyer_email'],
                        password=request.POST['password_2']
                    )

                    # Залогінь якщо все ок
                    authenticate_user = authenticate(request, username=user.username, password=request.POST.get('password_2'))

                    if authenticate_user:
                        login(request, authenticate_user)

                # Якщо все ок створи екземпряр замовдення
                print('все ок, створюю ордер')
                order_form.session_key = session_key
                order_form.buyer_name = form.cleaned_data['buyer_name']
                order_form.buyer_lastname = form.cleaned_data['buyer_lastname']
                order_form.buyer_tel = form.cleaned_data['buyer_tel']
                order_form.buyer_email = form.cleaned_data['buyer_email']
                order_form.pay_way = form.cleaned_data['pay_way']
                order_form.transporter = form.cleaned_data['transporter']
                order_form.area = form.cleaned_data['area']
                order_form.city = form.cleaned_data['city']
                order_form.department = form.cleaned_data['department']
                order_form.wish = form.cleaned_data['wish']
                order_form.save()

                product_baskets = Basket.objects.filter(session_key=session_key)

                # створення екземпляру купленого продукту та видали продукти з корзини
                for basket in product_baskets:
                    PurchasedProduct.objects.create(
                        session_key=session_key,
                        order=order_form,
                        image=basket.image,
                        id_product=basket.id_product,
                        title=basket.title,
                        price=basket.price,
                        number=basket.number,
                        total_price=basket.total_price
                    )

                    basket.delete()

                order_total_price = order_form.total_price
                shipping_address = order_form.department
                payee_name = str(order_form.buyer_name) + ' ' + str(order_form.buyer_lastname)

                # Відправ повідомлення
                subject = 'Реквізити для оплати замовлення на сайті "Al dente".'

                html_message = render_to_string(
                    'Performer/Requisites_for_payment.html', {'order_total_price': order_total_price, 'shipping_address': shipping_address,
                                                              'payee_name': payee_name})

                if order_form.pay_way == 'Приват24':
                    send_mail(subject, 'message', settings.EMAIL_HOST_USER, [request.POST.get('buyer_email')], html_message=html_message, fail_silently=False)

                    informational_message = 'На вашу поштову скриньку було відправлено повідомлення з реквізитами для оплати.'

                    return render(request, 'Performer/Successful_order.html', context={'informational_message': informational_message, 'shipping_address': shipping_address, 'payee_name': payee_name})

        return redirect(successful_order)


def successful_order(request):
    return render(request, 'Performer/Successful_order.html')


class Profile(View):
    def get(self, request):

        email = request.user.email

        orders = Order.objects.filter(buyer_email=email)

        products = PurchasedProduct.objects.all()

        fields_data = {
            'name': request.user.first_name,
            'last_name': request.user.last_name,
            'login': request.user.username,
            'email': request.user.email
        }

        form = ChangeSettings(fields_data)

        return render(request, 'Performer/Profile.html', context={'orders': orders, 'products': products, 'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = ChangeSettings(request.POST)
            if form.is_valid():
                user = request.user
                user.first_name = form.cleaned_data['name']
                user.last_name = form.cleaned_data['last_name']
                user.username = form.cleaned_data['login']
                user.email = form.cleaned_data['email']
                user.save()

                return redirect('/user_profile/')


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/user_profile/')
            else:
                error = 'Неправильний логін або пароль'
                products = Product.objects.all()
                return render(request, 'Performer/Home_page.html', context={'products': products, 'error': error})


def logout_user(request):
    logout(request)
    return redirect('/')


# Робота з ajax та json
def func(request):
    if request.method == 'POST':
        print('post')

        session_key = request.session.session_key

        if request.POST.get('delete'):

            product_id = request.POST.get('product_id')
            basket = Basket.objects.get(id_product=product_id)
            basket.delete()

        elif request.POST.get('update'):
            print('urdate')
            product_id = request.POST.get('product_id')
            product_number = request.POST.get('product_number')
            basket = Basket.objects.get(id_product=product_id)
            basket.number = int(product_number)
            basket.save()

        elif request.POST.get('create'):

            product_id = request.POST.get('product_id')
            product_image = request.POST.get('product_image')
            product_title = request.POST.get('product_title')
            product_price = request.POST.get('product_price')
            product_number = request.POST.get('product_number')

            product = Product.objects.get(id=product_id)

            basket, create = Basket.objects.get_or_create(
                session_key=session_key,
                product=product,
                id_product=int(product_id),
                image=product_image,
                title=product_title,
                price=float(product_price),
                defaults={'number': int(product_number)},
            )

            if create is False:
                basket.number += int(product_number)
                basket.save()

        product_list = list()
        sum_of_products = 0
        sum_of_price = 0

        for product in Basket.objects.filter(session_key=session_key):

            product_dict = dict()

            sum_of_products += product.number
            sum_of_price += product.total_price

            print(sum_of_products)

            product_dict['product_id'] = product.id_product
            product_dict['image'] = str(product.image)
            product_dict['title'] = product.title
            product_dict['price'] = product.price
            product_dict['number'] = product.number
            product_dict['total_price'] = product.total_price
            product_dict['sum_of_price'] = sum_of_price
            product_dict['sum_of_products'] = sum_of_products
            product_dict['product_url'] = product.product.get_absolute_url()

            if request.POST.get('update'):
                product_dict['action'] = 'update'
            else:
                product_dict['action'] = 'create_delete'

            print(product_dict)

            product_list.append(product_dict)

            print(product_list)

        data = {key: value for (key, value) in zip(range(0, len(product_list)), product_list)}
        print(data)

        return JsonResponse(data)

