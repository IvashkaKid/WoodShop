"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from .forms import AnketaForm

from django.db import models
from .models import Blog

from .models import Comment 
from .forms import CommentForm

from .forms import BlogForm

from .models import Category

from .models import Product

from .models import CartItem

from .models import Status

from .models import Order

from .models import OrderItem


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Полезные ресурсы',
            'year':datetime.now().year,
        }
    )

def pool(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    visit = {'1': 'В течение месяца', '2': 'Больше месяца назад', '3': 'Ещё ничего не покупал'}

    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['phone'] = form.cleaned_data['phone']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['visit'] = visit[form.cleaned_data['visit']]
            data['notice'] = 'Да' if form.cleaned_data['notice'] else 'Нет'
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = AnketaForm()

    return render(
        request,
        'app/pool.html',
        {
            'form': form, 
            'data': data
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        
        if regform.is_valid():  # валидация полей формы
            reg_f = regform.save(commit=False)  # не сохраняем автоматически данные формы
            reg_f.is_staff = False  # запрещен вход в административный раздел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации
            reg_f.save()  # сохраняем изменения после добавления данных
            return redirect('home')  # переадресация на главную страницу после регистрации

    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных нового пользователя
    
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def blog(request):
    posts = Blog.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Новости',
            'posts': posts,
            'year': datetime.now().year,
        }
    )
def blogpost(request, parametr):
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()
            return redirect('blog')
    else:
        blogform = BlogForm()
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Видео',
            'year':datetime.now().year,
        }
    )

def catalog(request):
    categories = Category.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/catalog.html',
        {
            'categories': categories,
            'year': datetime.now().year,
        }
    )

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(
        request,
        'app/product_detail.html',
        {
            'product': product,
            'year': datetime.now().year,
        }
    )

def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        if not cart_items:
            return redirect('cart')

        status = Status.objects.get(name='Новый')  # Предполагается, что у вас есть статус "Новый"
        order = Order.objects.create(user=request.user, total_price=total_price, status=status)

        # Создание позиций заказа
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_time_order=item.product.price
            )

        # Очистка корзины
        cart_items.delete()

        return redirect('order_detail', order_id=order.id)

    return render(
        request,
        'app/cart.html',
        {
            'cart_items': cart_items,
            'total_price': total_price,
            'year': datetime.now().year,
        }
    )

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()
    else:
        # Handle anonymous user cart using session
        cart = request.session.get('cart', {})
        cart_item_id = str(product.id)
        if cart_item_id in cart:
            cart[cart_item_id]['quantity'] += quantity
        else:
            cart[cart_item_id] = {'quantity': quantity}
        request.session['cart'] = cart

    # Обновляем информацию о корзине
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = [
            {'product': Product.objects.get(id=int(item_id)), 'quantity': details['quantity']}
            for item_id, details in request.session.get('cart', {}).items()
        ]

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Возвращаем HTML-ответ с уведомлением
    return render(
        request,
        'app/add_to_cart_notification.html',
        {
            'product_name': product.name,
            'cart_items': cart_items,
            'total_price': total_price,
            'year': datetime.now().year,
        }
    )

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.user.is_authenticated and cart_item.user == request.user:
        cart_item.delete()
    return redirect('cart')

def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.user.is_authenticated and cart_item.user == request.user:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'app/order_detail.html', {'order': order, 'order_items': order_items})


def order_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-order_date')
    else:
        orders = []

    return render(
        request,
        'app/order_list.html',
        {
            'orders': orders,
            'year': datetime.now().year,
        }
    )

def manage_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(
        request,
        'app/manage_orders.html',
        {
            'orders': orders,
            'year': datetime.now().year,
        }
    )

def manage_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    statuses = Status.objects.all()

    if request.method == 'POST':
        new_status_id = request.POST.get('status')
        new_status = get_object_or_404(Status, id=new_status_id)
        order.status = new_status
        order.save()
        return redirect('manage_order_detail', order_id=order.id)

    return render(
        request,
        'app/manage_order_detail.html',
        {
            'order': order,
            'order_items': order_items,
            'statuses': statuses,
            'year': datetime.now().year,
        }
    )

def home(request):
    latest_blogs = Blog.objects.order_by('-posted')[:3]
    return render(request, 'app/index.html', {'latest_blogs': latest_blogs})