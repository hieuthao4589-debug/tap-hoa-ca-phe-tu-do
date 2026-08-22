from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Category, Order, OrderDetail


def home(request, category_id=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    current_category = None
    if category_id:
        from django.shortcuts import get_object_or_404

        current_category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=current_category)
    return render(
        request,
        "index.html",
        {
            "products": products,
            "categories": categories,
            "current_category": current_category,
        },
    )


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def add_to_cart(request, product_id):
    if request.method == "POST":
        size = request.POST.get("size", "")
        ice = request.POST.get("ice", "Đá chung")
        sweetness = request.POST.get("sweetness", "Bình thường")

        product = Product.objects.get(id=product_id)

        final_price = product.price
        if size:
            size_obj = product.sizes.filter(name=size).first()
            if size_obj:
                final_price += size_obj.price

        cart_key = f"{product_id}_{size}_{ice}_{sweetness}"
        cart = request.session.get("cart", {})

        if cart_key in cart:
            cart[cart_key]["quantity"] += 1
        else:
            cart[cart_key] = {
                "product_id": product_id,
                "name": product.name,
                "price": final_price,
                "size": size,
                "ice": ice,
                "sweetness": sweetness,
                "quantity": 1,
                "image": product.image.url if product.image else "",
            }

        request.session["cart"] = cart

    return redirect("/#menu")


def view_cart(request):
    cart = request.session.get("cart", {})
    total_price = 0
    try:
        for item in cart.values():
            total_price += item["price"] * item["quantity"]
    except (TypeError, KeyError):
        cart = {}
        request.session["cart"] = cart
        total_price = 0

    return render(
        request, "cart.html", {"cart_items": cart, "total_price": total_price}
    )


def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("home")

    # Bắt phương thức thanh toán từ form gửi sang
    payment_method = request.POST.get("paymentMethod", "cash")
    request.session["last_payment"] = payment_method

    total_price = sum(item["price"] * item["quantity"] for item in cart.values())

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total_price=total_price,
        status="Pending",
    )

    for key, item in cart.items():
        OrderDetail.objects.create(
            order=order,
            product_name=item["name"],
            size=item.get("size", ""),
            ice=item.get("ice", ""),
            sweetness=item.get("sweetness", ""),
            quantity=item["quantity"],
            price=item["price"],
        )

    request.session["cart"] = {}
    order_details = OrderDetail.objects.filter(order=order)

    # Gửi cả hóa đơn lẫn danh sách món sang giao diện
    return render(
        request, "success.html", {"order": order, "order_details": order_details}
    )


def update_cart(request, cart_key, action):
    cart = request.session.get("cart", {})
    if cart_key in cart:
        if action == "plus":
            cart[cart_key]["quantity"] += 1
        elif action == "minus":
            cart[cart_key]["quantity"] -= 1
            if cart[cart_key]["quantity"] <= 0:
                del cart[cart_key]
        request.session["cart"] = cart
    return redirect("/cart/")


from .models import UserProfile  # Nhớ kiểm tra xem đã có dòng này ở đầu file chưa nha


def profile_view(request):
    # Bắt buộc phải đăng nhập mới được xem trang này
    if not request.user.is_authenticated:
        return redirect("login_view")

    # Tìm profile của khách, nếu chưa có thì hệ thống tự tạo mới luôn
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # 1. Lưu thông tin cơ bản
        request.user.first_name = request.POST.get("full_name", "")
        request.user.email = request.POST.get("email", "")
        request.user.save()

        # 2. Lưu thông tin ship hàng
        profile.phone = request.POST.get("phone", "")
        profile.address = request.POST.get("address", "")
        profile.gender = request.POST.get("gender", "")

        dob = request.POST.get("dob")
        if dob:
            profile.dob = dob

        profile.save()
        return redirect("profile_view")  # Lưu xong thì tải lại trang cho mới

    return render(request, "profile.html", {"profile": profile})


def about_view(request):
    return render(request, "about.html")
