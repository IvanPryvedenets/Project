$(document).ready(function(){
    console.log('hi')

    $(window).scroll(function () {
        if ($(this).scrollTop() >= 120) {
            $('.user-place').slideUp(100)
            $('.menu').css('top', 0)
        } else {
            $('.user-place').slideDown(100)
            $('.menu').css('top', 20)
        }
    })

//    ajax функція для видалення та додавання
    function AjaxEngine(form, data){

        var MethodForm = form.attr('method');
        var ActionForm = form.attr('action');

        $.ajax({
            type: MethodForm,
            url: ActionForm,
            data: data,
            dataType: 'json',
            success: function(data){
                console.log(data)
                console.log('success')

                if (data['0']){

//                якщо в реквесті є клбч зі значенням update
                    if (data['0']['action'] == 'update'){
                        $.each(data, function(key, value){

    //                        Оновлюється загальна кількість продуктів
                            $('.product-basket-number-wrapper').remove()

                            $('.basket-wrapper').append('<div class="product-basket-number-wrapper">' +
                                                                '<span class="product-number">' + value['sum_of_products'] + '</span>' +
                                                            '</div>')

    //                    Зачисти потім встав нові значення загальної ціни в корзині та сторінці корзини
                            $('.cart-buttons').remove()
                            $('.cart-total-price').remove()


    //                    Встав кнопки та ціну в корзину
                            $('.cart').append('<div class="cart-total-price">' +
                                                    '<span>Загалом: ' + value['sum_of_price'] + '</span>' +
                                                '</div>')

                            $('.cart').append('<div class="cart-buttons">' +
                                                    '<a href="/cart/"><button class="btn btn-primary" type="button">Переглянути корзину</button></a>' +
                                                    '<a href="/checkout/"><button class="btn btn-primary" type="button">Оформити замовлення</button></a>' +
                                                '</div>')

    //                        Загальна ціна на сторінці корзини
                            $('.transition-to-checkout').append('<div class="cart-total-price">' +
                                                                    '<span>Загалом: ' + value['sum_of_price'] + '</span>' +
                                                                '</div>' +

                                                                '<div class="cart-buttons">' +
                                                                    '<a href="/checkout/"><button class="btn btn-primary" type="button">Оформити замовлення</button></a>' +
                                                                '</div>')

                        })


    //                якщо в реквесті є клбч зі значенням delete або create
                    } else if (data['0']['action'] == 'create_delete') {
                        console.log('create_delete')

    //                Зачисти контейнер з продуктами в корзині
                    $('.selected-product-container').html('')
                    $('.cart-product-wrapper').html('')



                    $.each(data, function(key, value){
                        console.log('ok')
    //                    Спочатку очисти а потім встав
                        $('.product-basket-number-wrapper').remove()

                        if (value['sum_of_products']){
                            $('.basket-wrapper').append('<div class="product-basket-number-wrapper">' +
                                                            '<span class="product-number">' + value['sum_of_products'] + '</span>' +
                                                        '</div>')
                        }

    //                    Заповни контейнер з продуктами
                        $('.selected-product-container').append('<div class="selected-product">' +
                                                                    '<span class="delete-selected-product" data-product_id="' + value['product_id'] + '">&#215;</span>' +
                                                                    '<img class="selected-product-image" src="' + value['image'] + '">' +
                                                                    '<a class="title" href="' + value['product_url'] + '"><h6>' + value['title'] + '</h6></a>' +
                                                                    '<div class="selected-product-price-info">' +
                                                                        '<span>' + value['price'] + ' грн' + '</span>' +
                                                                        '<span>' + '&#215;' + '</span>' +
                                                                        '<span>' + value['number'] + '</span>' +
                                                                    '</div>' +
                                                                '</div>')

    //                    Заповнити контент корзини
                        $('.cart-product-wrapper').append('<div class="cart-product">' +
                                                                '<span class="delete-selected-product" data-product_id="' + value['product_id'] + '">&#215;</span>' +
                                                                '<img class="cart-product-image" src="' + value['image'] + '">' +
                                                                '<div class="cart-product-title"><h4 class="title>"><a href="' + value['url'] + '">' + value['title'] + '</a></h4></div>' +
                                                                '<div class="cart-product-price">' + value['price'] + ' грн</div>' +
                                                                '<input class="form-control" type="number" value="' + value['number'] + '" min="1">' +
                                                                '<div class="cart-product-total_price">' + value['total_price'] + ' грн</div>' +
                                                            '</div>')

    //                    Зачисти потім встав нові значення загальної ціни
                        $('.cart-buttons').remove()
                        $('.cart-total-price').remove()

    //                    Встав кнопки та ціну
                        $('.cart').append('<div class="cart-total-price">' +
                                                '<span>Загалом: ' + value['sum_of_price'] + '</span>' +
                                            '</div>')

                        $('.cart').append('<div class="cart-buttons">' +
                                                '<a href="/cart/"><button class="btn btn-primary" type="button">Переглянути корзину</button></a>' +
                                                '<a href="/checkout/"><button class="btn btn-primary" type="button">Оформити замовлення</button></a>' +
                                            '</div>')

                        $('.transition-to-checkout').append('<div class="cart-total-price">' +
                                                                '<span>Загалом: ' + value['sum_of_price'] + '</span>' +
                                                            '</div>' +

                                                            '<div class="cart-buttons">' +
                                                                '<a href="/checkout/"><button class="btn btn-primary" type="button">Оформити замовлення</button></a>' +
                                                            '</div>')

                        })

                    }

//                Якщо словник порожній очисти кількість продуктів, кнопки, загальну ціну та встав 'корзина порожня'
                } else {
                    $('.product-basket-number-wrapper').remove()
                    $('.cart-buttons').remove()
                    $('.cart-total-price').remove()
                    $('.selected-product-container').html('<h6 class="title" style="position: relative; width: 100%; margin: 5px 0 5px 0; text-align: center; top: 0; left: 0;">Кошик порожній</h6>')
                    $('.cart-product-wrapper').html('<h6 class="title" style="position: relative; width: 100%; margin: 5px 0 5px 0; text-align: center; top: 5px; left: 0;">Кошик порожній</h6>')
                    $('.cart-table').remove()
                }

            },

            error: function(){
                console.log('error')
            }
        })

    }



//    Додавання продуктів в корзину
    $('.add-product-to-basket').on('submit', function(e){
        e.preventDefault();

        var data = {}

        var form = $(this);

        console.log(form);

        var product_number = form.children('#product-info-number').val();

        if (product_number == undefined){
            product_number = 1
        }

        console.log(product_number)

        var button = form.children('#btn-primary')

        var csrf_token = $('.add-product-to-basket [name="csrfmiddlewaretoken"]').val()
        var product_id = button.data('product_id')
        var product_image = button.data('product_image')
        var product_title = button.data('product_title')
        var product_price = button.data('product_price')

        data['create'] = 'create'

        data['csrfmiddlewaretoken'] =  csrf_token
        data['product_id'] = product_id
        data['product_image'] = product_image
        data['product_title'] = product_title
        data['product_price'] = product_price
        data['product_number'] = product_number


        AjaxEngine(form, data)

    });

    //Видалення продуктів з корзини
    $(document).on('click', '.delete-selected-product', function () {

        var form = $('.cart-form')

        console.log(form)

        var csrf_token = $('.cart-form [name="csrfmiddlewaretoken"]').val()
        var product_id = $(this).data('product_id')

        data = {}

        data['delete'] = 'delete'

        data['csrfmiddlewaretoken'] = csrf_token
        data['product_id'] = product_id

        AjaxEngine(form, data)
    });


//     Зміна кількості продуктів на сторінці корзини
    $(document).on('change', '#form-control', function () {

        var form = $('.cart-form')

        var csrf_token = $('.cart-form [name="csrfmiddlewaretoken"]').val()
        var product_id = $(this).parent('.cart-product').children('.delete-selected-product').data('product_id')
        var product_number = $(this).val()

        var price =  $(this).parent('.cart-product').children('.cart-product-price').text().replace('грн', '')

        var total_price = parseInt(price) * parseInt(product_number) + '.00 грн'

        console.log(total_price)

        $('.selected-product').children('.delete-selected-product').each(function(){
            if ($(this).data('product_id') == product_id)
                $(this).parent('.selected-product').children('.selected-product-price-info').html('<span>' + price + ' грн</span>' +
                                                                                                    '<span>&#215;</span>' +
                                                                                                    '<span class="selected-product-number">' + product_number +'</span>')
        })

        $(this).parent('.cart-product').children('.cart-product-total_price').html(total_price)



////       оновлюється кількість продуктів в корзині
//        $('.selected-product-price-info').children('.selected-product-number').text(product_number)


        data = {}

        data['update'] = 'update'

        data['csrfmiddlewaretoken'] = csrf_token
        data['product_id'] = product_id
        data['product_number'] = product_number

        console.log(form)

        AjaxEngine(form, data)
    });


//    відстежується кількість натискань на чекбокс. Парне - виводиться форма, не парне число видаляється з блоку форма
    var tracking_user_form = 0
    $('.create-user-checkbox').click(function(){
        tracking_user_form += 1

        if(tracking_user_form & 1) {
            $('.create-user-forms').css('display', 'block')

            $('.user-form').appendTo('.create-user-forms')

            $('.user-form').css('display', 'block')

        } else {
            $('.create-user-forms').css('display', 'none')

            $('.user-form').appendTo('.checkout-content-wrapper')

            $('.user-form').css('display', 'none')
        }
    })


    $(document).on('click', '#checkout-submit', function(e){
        var password_1 = $(this).parent('.checkout-form').find('.user-form').children('p').children("[name='password_1']").val()

        var password_2 = $(this).parent('.checkout-form').find('.user-form').children('p').children("[name='password_2']").val()

        if (password_1 !== password_2){
            e.preventDefault()
            alert('Паролі в двох полях не збігаються. Повторіть спробу.')
        }
    })


    $('.product-arrow').click(function(){
        var name = parseInt($(this).attr('name'))

        if (name == 0) {
            console.log(name)
            $(this).css('transform', 'rotate(135deg)')
            name = 1
            $(this).attr('name', name)
            $(this).parent('.order-box').parent('.order-boxes').children('.purchased-product-content').slideDown()

        } else {
            $(this).css('transform', 'rotate(45deg)')
            name = 0
            $(this).attr('name', name)
            $(this).parent('.order-box').parent('.order-boxes').children('.purchased-product-content').slideUp()
        }
    })


})
