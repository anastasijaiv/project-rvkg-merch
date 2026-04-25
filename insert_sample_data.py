import sqlite3

DB_PATH = "database.db"

# ------------------
# ORIGINAL HARDCODED DATA
# ------------------

COLLECTIONS = {
    "aw2022": {
        "title": "Balta kolekcija",
        "items": [
            {"image": "/static/pictures/whitee_hoodie.png", "name": "Balts džemperis",
             "price": "55.99€", "description": "Augstas kvalitātes kokvilnas pelēks džemperis ar RVKģ logo",
             "category": "tops"},
            {"image": "/static/pictures/white_hoodie.png", "name": "Pelēks džemperis",
             "price": "25.99€", "description": "Elpojošs kokvilnas balts džemperis aktīvam ar RKVģ logo",
             "category": "tops"},
            {"image": "/static/pictures/white_tshirt.png", "name": "Balts t-krekls",
             "price": "19.99€", "description": "Ērts, balts t-krekls vasaras sezonai",
             "category": "tops"},
            {"image": "/static/pictures/white_bag.png", "name": "Balts šoperis",
             "price": "22.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/white_cup.png", "name": "Balts krūze",
             "price": "14.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/white_hat.png", "name": "Balta cepure",
             "price": "22.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/white_longsleeve_man.png", "name": "Balts garās piedurknes krekls vīriešiem",
             "price": "19.99€", "description": "Garās piedurknes krekls visām sezonām vīrišiem",
             "category": "tops"},
            {"image": "/static/pictures/white_longsleeve_woman.png", "name": "Balts garās piedurknes krekls sievietem",
             "price": "19.99€", "description": "Garās piedurknes krekls visām sezonām sievietem",
             "category": "tops"},
            {"image": "/static/pictures/white_socks.png", "name": "Baltas zēķes",
             "price": "9.99€", "description": "ADD", "category": "socks"},
            {"image": "/static/pictures/white_cap.png", "name": "Balta vasaras cepure",
             "price": "9.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/white_pants.png", "name": "Balta bikses",
             "price": "49.99€", "description": "ADD", "category": "pants"},
            {"image": "/static/pictures/white_pencil.png", "name": "Balts penalis",
             "price": "19.99€", "description": "ADD", "category": "accessories"},
        ],
    },

    "ss2023": {
        "title": "Melna kolekcija",
        "items": [
            {"image": "/static/pictures/black_hoddie.png", "name": "Melns džemperis",
             "price": "55.99€", "description": "Viegls un elpojošs melns džemperis",
             "category": "tops"},
            {"image": "/static/pictures/black_tshirt.png", "name": "Melns t-krekls",
             "price": "21.99€", "description": "Ērts sporta melna t-krekls aktīvām nodarbībām",
             "category": "tops"},
            {"image": "/static/pictures/black_bag.png", "name": "Melnais šoperis",
             "price": "22.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/black_cup.png", "name": "Melna krūze",
             "price": "14.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/black_socks.png", "name": "Melnas zēķes",
             "price": "9.99€", "description": "ADD", "category": "socks"},
            {"image": "/static/pictures/black_longsleeve_man.png", "name": "Melns garās piedurknes krekls vīriešiem",
             "price": "19.99€", "description": "Garās piedurknes krekls visām sezonām vīrišiem",
             "category": "tops"},
            {"image": "/static/pictures/black_longsleeve_woman.png", "name": "Melns garās piedurknes krekls sievietem",
             "price": "19.99€", "description": "Garās piedurknes krekls visām sezonām sievietem",
             "category": "tops"},
            {"image": "/static/pictures/black_hat.png", "name": "Melna cepure",
             "price": "22.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/black_cap.png", "name": "Melna vasaras cepure",
             "price": "9.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/black_pants.png", "name": "Melnas bikses",
             "price": "49.99€", "description": "ADD", "category": "pants"},
            {"image": "/static/pictures/black_pencil.png", "name": "Melns penalis",
             "price": "19.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/black_ziphoodie.png", "name": "Melns džemperis ar rāvējslēdzēju",
             "price": "59.99€", "description": "ADD", "category": "tops"},
        ],
    },

    "aw2024": {
        "title": "Zila kolekcija",
        "items": [
            {"image": "/static/pictures/blue_hoodie.png", "name": "Zils džemperis",
             "price": "55.99€", "description": "Silta ziemas zils džemperis",
             "category": "tops"},
            {"image": "/static/pictures/blue_tshirt.png", "name": "Zils t-krekls",
             "price": "19.99€", "description": "Stilīgs parka zils t-krekls",
             "category": "tops"},
            {"image": "/static/pictures/blue_bag.png", "name": "Zils šoperis",
             "price": "22.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/blue_cup.png", "name": "Zila krūze",
             "price": "14.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/blue_hat.png", "name": "Zila cepure",
             "price": "22.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/blue_socks.png", "name": "Zilas zēķes",
             "price": "9.99€", "description": "ADD", "category": "socks"},
            {"image": "/static/pictures/blue_longsleeve_man.png", "name": "Zils garās piedurknes krekls vīriešiem",
             "price": "19.99€", "description": "Garās piedurknes krekls visām sezonām vīrišiem",
             "category": "tops"},
            {"image": "/static/pictures/blue_longsleeve_woman.png", "name": "Zils garās piedurknes krekls sievietem",
             "price": "19.99€", "description": "Garās piedurknes krekls visām sezonām sievietem",
             "category": "tops"},
            {"image": "/static/pictures/blue_cap.png", "name": "Zila vasaras cepure",
             "price": "9.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/blue_pants.png", "name": "Zilas bikses",
             "price": "49.99€", "description": "ADD", "category": "pants"},
            {"image": "/static/pictures/blue_pencil.png", "name": "Zils penalis",
             "price": "19.99€", "description": "ADD", "category": "accessories"},
            {"image": "/static/pictures/blue_ziphoodie.png", "name": "Zils džemperis ar rāvējslēdzēju",
             "price": "59.99€", "description": "ADD", "category": "tops"},
        ],
    },
}

# ------------------
# INSERT INTO DATABASE
# ------------------

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for code, collection in COLLECTIONS.items():
    # Insert collection
    cursor.execute("""
        INSERT OR IGNORE INTO collections (name, code, description)
        VALUES (?, ?, ?)
    """, (collection["title"], code, collection["title"]))

    cursor.execute("SELECT id FROM collections WHERE code = ?", (code,))
    collection_id = cursor.fetchone()[0]

    for item in collection["items"]:
        price = float(item["price"].replace("€", ""))

        cursor.execute("""
            INSERT OR IGNORE INTO products
            (name, category, image_url, collection_id, price, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item["name"],
            item["category"],
            item["image"],
            collection_id,
            price,
            item["description"]
        ))

conn.commit()
conn.close()

print("✅ All collections and products inserted successfully!")
