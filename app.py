import os

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash
)

from flask import jsonify
from services.gemini_service import ask_gemini

from google_sheets import (
    get_menu,
    get_menu_item,
    add_order,
    add_order_item,
    add_order_summary,
    generate_order_id,
    add_contact
)

from datetime import datetime

# ==========================================================
# Flask App Configuration
# ==========================================================

app = Flask(__name__)

app.secret_key = "restaurant_secret_key_2026"

app.config["SESSION_PERMANENT"] = False

# ==========================================================
# SESSION CART FUNCTIONS
# ==========================================================

def get_cart():

    """
    Returns cart stored in session.
    Creates empty cart if not available.
    """

    if "cart" not in session:
        session["cart"] = {}

    return session["cart"]


def save_cart(cart):

    """
    Save updated cart back to session.
    """

    session["cart"] = cart
    session.modified = True


def get_cart_items():

    """
    Returns all cart items as list.
    """

    cart = get_cart()

    return list(cart.values())


def get_cart_count():

    """
    Returns total quantity of all products.
    """

    cart = get_cart()

    return sum(item["quantity"] for item in cart.values())


def get_cart_total():

    """
    Returns total bill amount.
    """

    cart = get_cart()

    return round(

        sum(

            item["price"] * item["quantity"]

            for item in cart.values()

        ),

        2

    )


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
def home():

    menu = get_menu()

    featured = menu[:6]

    return render_template(

        "home.html",

        featured_menu=featured,

        cart_count=get_cart_count()

    )


# ==========================================================
# MENU PAGE
# ==========================================================

@app.route("/menu")
def menu_page():

    menu = get_menu()

    return render_template(

        "menu.html",

        menu=menu,

        cart_count=get_cart_count()

    )


# ==========================================================
# SEARCH FOOD
# ==========================================================

@app.route("/search")
def search():

    keyword = request.args.get("q", "").strip().lower()

    menu = get_menu()

    if keyword:

        results = [

            item

            for item in menu

            if keyword in item["name"].lower()

        ]

    else:

        results = menu

    return render_template(

        "menu.html",

        menu=results,

        cart_count=get_cart_count(),

        search=keyword

    )


# ==========================================================
# FILTER BY CATEGORY
# ==========================================================

@app.route("/category/<category>")
def category(category):

    menu = get_menu()

    filtered = [

        item

        for item in menu

        if item["category"].lower() == category.lower()

    ]

    return render_template(

        "menu.html",

        menu=filtered,

        cart_count=get_cart_count(),

        category=category

    )


# ==========================================================
# ABOUT PAGE
# ==========================================================

@app.route("/about")
def about():

    return render_template(

        "about.html",

        cart_count=get_cart_count()

    )


# ==========================================================
# CONTACT PAGE
# ==========================================================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        email = request.form.get("email", "").strip()

        message = request.form.get("message", "").strip()

        if not name or not email or not message:

            flash(

                "Please fill all fields.",

                "danger"

            )

            return redirect(url_for("contact"))

        try:

            add_contact(

                name,

                email,

                message

            )

            flash(

                "Message sent successfully.",

                "success"

            )

        except Exception:

            flash(

                "Unable to send your message.",

                "danger"

            )

        return redirect(url_for("contact"))

    return render_template(

        "contact.html",

        cart_count=get_cart_count()

    )

    # ==========================================================
# ADD TO CART
# ==========================================================

@app.route("/add-to-cart/<int:item_id>")
def add_to_cart(item_id):

    item = get_menu_item(item_id)

    if item is None:

        flash("Food item not found.", "danger")

        return redirect(url_for("menu_page"))

    cart = get_cart()

    item_key = str(item_id)

    if item_key in cart:

        cart[item_key]["quantity"] += 1

    else:

        cart[item_key] = {

            "id": item["id"],
            "name": item["name"],
            "price": float(item["price"]),
            "image": item["image"],
            "rating": item["rating"],
            "category": item["category"],
            "quantity": 1

        }

    save_cart(cart)

    flash(f'{item["name"]} added to cart.', "success")

    return redirect(request.referrer or url_for("menu_page"))


# ==========================================================
# CART PAGE
# ==========================================================

@app.route("/cart")
def cart_page():

    return render_template(

        "cart.html",

        cart=get_cart_items(),

        total=get_cart_total(),

        cart_count=get_cart_count()

    )


# ==========================================================
# INCREASE QUANTITY
# ==========================================================

@app.route("/increase/<int:item_id>")
def increase_quantity(item_id):

    cart = get_cart()

    item_key = str(item_id)

    if item_key in cart:

        cart[item_key]["quantity"] += 1

        save_cart(cart)

    return redirect(url_for("cart_page"))


# ==========================================================
# DECREASE QUANTITY
# ==========================================================

@app.route("/decrease/<int:item_id>")
def decrease_quantity(item_id):

    cart = get_cart()

    item_key = str(item_id)

    if item_key in cart:

        cart[item_key]["quantity"] -= 1

        if cart[item_key]["quantity"] <= 0:

            del cart[item_key]

        save_cart(cart)

    return redirect(url_for("cart_page"))


# ==========================================================
# REMOVE ITEM
# ==========================================================

@app.route("/remove/<int:item_id>")
def remove_item(item_id):

    cart = get_cart()

    item_key = str(item_id)

    if item_key in cart:

        removed_name = cart[item_key]["name"]

        del cart[item_key]

        save_cart(cart)

        flash(f"{removed_name} removed from cart.", "warning")

    return redirect(url_for("cart_page"))


# ==========================================================
# CLEAR CART
# ==========================================================

@app.route("/clear-cart")
def clear_cart():

    session["cart"] = {}

    session.modified = True

    flash("Cart cleared successfully.", "info")

    return redirect(url_for("cart_page"))


# ==========================================================
# MINI CART (Optional)
# ==========================================================

@app.route("/mini-cart")
def mini_cart():

    return render_template(

        "mini_cart.html",

        cart=get_cart_items(),

        total=get_cart_total(),

        cart_count=get_cart_count()

    )


# ==========================================================
# CART SUMMARY API (Optional)
# ==========================================================

@app.route("/cart-summary")
def cart_summary():

    return {

        "items": get_cart_items(),

        "count": get_cart_count(),

        "total": get_cart_total()

    }

    # ==========================================================
# CHECKOUT
# ==========================================================

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    cart_items = get_cart_items()

    # Prevent checkout with empty cart
    if not cart_items:

        flash("Your cart is empty.", "warning")

        return redirect(url_for("menu_page"))

    total = get_cart_total()

    if request.method == "POST":

        customer_name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        payment = request.form.get("payment", "").strip()

        # -----------------------------
        # Basic Validation
        # -----------------------------

        if not customer_name:

            flash("Customer name is required.", "danger")

            return redirect(url_for("checkout"))

        if not phone:

            flash("Phone number is required.", "danger")

            return redirect(url_for("checkout"))

        if not address:

            flash("Delivery address is required.", "danger")

            return redirect(url_for("checkout"))

        if payment == "":

            flash("Please select payment method.", "danger")

            return redirect(url_for("checkout"))

        # -----------------------------
        # Generate Order ID
        # -----------------------------

        try:

            order_id = generate_order_id()

        except Exception as e:

            flash(f"Unable to generate Order ID: {e}", "danger")

            return redirect(url_for("checkout"))

        # -----------------------------
        # Save Main Order
        # -----------------------------

        try:

            add_order(

                order_id,

                customer_name,

                phone,

                email,

                address,

                payment,

                total

            )

        except Exception as e:

            flash(f"Unable to save order: {e}", "danger")

            return redirect(url_for("checkout"))

        # -----------------------------
        # Save Order Items
        # -----------------------------

        items_summary = []

        try:

            for item in cart_items:

                add_order_item(

                    order_id,

                    item["name"],

                    item["quantity"],

                    item["price"]

                )

                items_summary.append(

                    f'{item["name"]} x{item["quantity"]}'

                )

        except Exception as e:

            flash(f"Unable to save order items: {e}", "danger")

            return redirect(url_for("checkout"))

        # -----------------------------
        # Save Order Summary
        # -----------------------------

        try:

            add_order_summary(

                order_id,

                customer_name,

                phone,

                email,

                address,

                payment,

                ", ".join(items_summary),

                total

            )

        except Exception as e:

            flash(f"Unable to save order summary: {e}", "danger")

            return redirect(url_for("checkout"))

        # -----------------------------
        # Clear Session Cart
        # -----------------------------

        session["cart"] = {}

        session.modified = True

        flash("Order placed successfully!", "success")

        # -----------------------------
        # Confirmation Page
        # -----------------------------

        return render_template(

            "order_confirmation.html",

            order_id=order_id,

            customer_name=customer_name,

            phone=phone,

            email=email,

            address=address,

            payment=payment,

            total=total,

            items=items_summary,

            order_date=datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"),

            cart_count=0

        )

    return render_template(

        "checkout.html",

        cart=cart_items,

        total=total,

        cart_count=get_cart_count()

    )
    
    # ==========================================================
# AI CHATBOT API
# ==========================================================

@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No JSON data received."
            }), 400

        message = data.get("message", "").strip()

        if message == "":
            return jsonify({
                "success": False,
                "message": "Message cannot be empty."
            }), 400

        reply = ask_gemini(message)

        return jsonify({
            "success": True,
            "data": {
                "reply": reply
            }
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

        
    # ==========================================================
# CONTEXT PROCESSOR
# Makes cart_count available in every template
# ==========================================================

@app.context_processor
def inject_global_variables():

    return {

        "cart_count": get_cart_count()

    }


# ==========================================================
# CACHE CONTROL
# Prevent browser caching after checkout
# ==========================================================

@app.after_request
def add_header(response):

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, "
        "post-check=0, pre-check=0, max-age=0"
    )

    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route("/health")
def health():

    return {

        "status": "OK",

        "application": "Restaurant Ordering System"

    }


# ==========================================================
# ERROR 404
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html"

    ), 404


# ==========================================================
# ERROR 500
# ==========================================================

@app.errorhandler(500)
def internal_server_error(error):

    return render_template(

        "500.html"

    ), 500



# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )