from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import sqlite3
from werkzeug.serving import WSGIRequestHandler
import os

app = Flask(__name__)
app.secret_key = "very-secret-key-change-later"

DB_PATH = "database.db"


# ------------------
# DATABASE HELPERS
# ------------------

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_admin_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_admin():
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO admins (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # admin already exists
    conn.close()


# ------------------
# QUIET REQUEST HANDLER
# ------------------

class QuietRequestHandler(WSGIRequestHandler):
    def log_request(self, code='-', size='-'):
        try:
            code = int(code)
        except ValueError:
            return
        if code >= 400:
            super().log_request(code, size)


# ------------------
# ROUTES
# ------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/collections")
def get_collections():
    collection_code = request.args.get("id")
    conn = get_db_connection()
    cursor = conn.cursor()

    # ---- single collection
    if collection_code:
        cursor.execute(
            "SELECT id, name FROM collections WHERE code = ?",
            (collection_code,)
        )
        collection = cursor.fetchone()

        if not collection:
            conn.close()
            return jsonify({"error": "Collection not found"}), 404

        cursor.execute("""
            SELECT name, category, image_url, price, description
            FROM products
            WHERE collection_id = ?
        """, (collection["id"],))

        items = []
        for row in cursor.fetchall():
            items.append({
                "image": row["image_url"],
                "name": row["name"],
                "price": f'{row["price"]:.2f}€',
                "description": row["description"],
                "category": row["category"]
            })

        conn.close()
        return jsonify({
            "title": collection["name"],
            "items": items
        })

    # ---- all collections
    cursor.execute("SELECT code, name FROM collections")
    collections = {}

    for row in cursor.fetchall():
        collections[row["code"]] = {
            "title": row["name"],
            "items": []
        }

    conn.close()
    return jsonify(collections)


# ---- PROMO CODE ROUTE ----
@app.route("/api/promo/<code>")
def check_promo(code):
    code = code.upper()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT code, discount, description FROM promo_codes WHERE code = ?",
        (code,)
    )
    promo = cursor.fetchone()
    conn.close()

    if not promo:
        return jsonify({"valid": False}), 404

    return jsonify({
        "valid": True,
        "code": promo["code"],
        "discount": promo["discount"],
        "description": promo["description"]
    })


# ------------------
# ADMIN AUTH
# ------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM admins WHERE username = ? AND password = ?",
            (username, password)
        )
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template("admin_login.html")


@app.route("/admin")
def admin_home():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    return redirect(url_for("admin_dashboard"))


# ------------------
# ADMIN DASHBOARD
# ------------------

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    search = request.args.get("q", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    # ---- Products
    if search:
        cursor.execute("""
            SELECT * FROM products
            WHERE
                name LIKE ?
                OR category LIKE ?
                OR description LIKE ?
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM products ORDER BY id DESC")

    products_rows = cursor.fetchall()
    products = [{
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "price": float(row["price"]),
        "description": row["description"],
        "image_url": row["image_url"],
        "collection_id": row["collection_id"]
    } for row in products_rows]

    # ---- Collections
    cursor.execute("SELECT id, name FROM collections")
    collections = [{"id": r["id"], "name": r["name"]} for r in cursor.fetchall()]

    # ---- Categories
    cursor.execute("""
        SELECT DISTINCT category
        FROM products
        WHERE category IS NOT NULL AND category != ''
        ORDER BY category
    """)
    categories = [r["category"] for r in cursor.fetchall()]

    # ---- Promo codes
    cursor.execute("SELECT * FROM promo_codes ORDER BY id DESC")
    promo_codes = [{
        "id": row["id"],
        "code": row["code"],
        "discount": row["discount"],
        "description": row["description"]
    } for row in cursor.fetchall()]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        products=products,
        collections=collections,
        categories=categories,
        promo_codes=promo_codes  # pass to template
    )


# ------------------
# PRODUCT CRUD
# ------------------

@app.route("/admin/add-product", methods=["POST"])
def add_product():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    name = request.form["name"]
    category = request.form["category"]
    image_url = request.form["image_url"]
    collection_id = request.form.get("collection_id") or None
    price = request.form["price"]
    description = request.form["description"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, category, image_url, collection_id, price, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, category, image_url, collection_id, price, description))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/update-product", methods=["POST"])
def update_product():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    product_id = request.form["id"]
    name = request.form["name"]
    category = request.form["category"]
    image_url = request.form["image_url"]
    collection_id = request.form.get("collection_id") or None
    price = request.form["price"]
    description = request.form["description"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products
        SET name=?, category=?, image_url=?, collection_id=?, price=?, description=?
        WHERE id=?
    """, (name, category, image_url, collection_id, price, description, product_id))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete-product", methods=["POST"])
def delete_product():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    product_id = request.form["id"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))


# ------------------
# PROMO CODE CRUD
# ------------------

@app.route("/admin/add-promo", methods=["POST"])
def add_promo():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    code = request.form["code"].upper()
    discount = int(request.form["discount"])
    description = request.form["description"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO promo_codes (code, discount, description)
        VALUES (?, ?, ?)
    """, (code, discount, description))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/edit-promo", methods=["POST"])
def edit_promo():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    promo_id = request.form["id"]
    code = request.form["code"].upper()
    discount = int(request.form["discount"])
    description = request.form["description"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE promo_codes
        SET code=?, discount=?, description=?
        WHERE id=?
    """, (code, discount, description, promo_id))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete-promo", methods=["POST"])
def delete_promo():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    promo_id = request.form["id"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM promo_codes WHERE id=?", (promo_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))


# ------------------
# LOGOUT
# ------------------

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("index"))


# ------------------
# APP START
# ------------------

if __name__ == "__main__":
    create_admin_table()
    insert_admin()

    if __name__ == "__main__":
        create_admin_table()
        insert_admin()

        port = int(os.environ.get("PORT", 8080))
        app.run(
            host ="0.0.0.0",
            port=port,
            debug=False,
            request_handler = QuietRequestHandler
        )
