from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/get_character/<int:char_id>')
def get_character(char_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT * FROM characters c
        LEFT JOIN races r ON c.race_id = r.race_id
        LEFT JOIN classes cl ON c.class_id = cl.class_id
        LEFT JOIN bag b ON c.character_id = b.character_id
        WHERE c.character_id = %s
    """, (char_id,))
    char = cur.fetchone()

    cur.close()
    conn.close()

    if not char:
        return jsonify({"error": "Character not found"}), 404

    return jsonify(char)

@app.route('/get_shop_items')
def get_shop_items():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    shop_data = {}

    for table in ['weapon', 'armor', 'artifact', 'consumable']:
        cur.execute(f"SELECT * FROM {table}")
        shop_data[table] = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(shop_data)

@app.route('/buy_item', methods=['POST'])
def buy_item():
    data = request.json
    char_id = data['char_id']
    item_type = data['item_type']  # weapon / armor / artifact / consumable
    item_id = data['item_id']

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Get item price
    if item_type == 'consumable':
        cur.execute("SELECT price FROM consumable WHERE c_id = %s", (item_id,))
    else:
        cur.execute(f"SELECT rarity FROM {item_type} WHERE {item_type[0]}_id = %s", (item_id,))
        rarity_to_price = {'Common': 20, 'Rare': 50, 'Epic': 100, 'Legend': 200}
        rarity_row = cur.fetchone()
        if not rarity_row:
            return jsonify({"error": "Item not found"}), 404
        price = rarity_to_price[rarity_row['rarity']]

    if item_type == 'consumable':
        price_row = cur.fetchone()
        if not price_row:
            return jsonify({"error": "Item not found"}), 404
        price = price_row['price']

    # Get character gold
    cur.execute("SELECT gold FROM characters WHERE character_id = %s", (char_id,))
    char = cur.fetchone()
    if not char or char['gold'] < price:
        return jsonify({"error": "Not enough gold"}), 400

    # Deduct gold
    new_gold = char['gold'] - price
    cur.execute("UPDATE characters SET gold = %s WHERE character_id = %s", (new_gold, char_id))

    # Add item to bag
    slot_column = get_empty_slot_column(cur, item_type, char_id)
    if not slot_column:
        return jsonify({"error": "No empty slot for this item type"}), 400

    cur.execute(f"""
        UPDATE bag SET {slot_column} = %s WHERE character_id = %s
    """, (item_id, char_id))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"success": True, "new_gold": new_gold})

def get_empty_slot_column(cur, item_type, char_id):
    slot_prefix = {
        'weapon': 'w_',
        'armor': 'a_',
        'artifact': 'art_',
        'consumable': 'consumable_'
    }

    if item_type == 'consumable':
        # Find an existing consumable with same ID or empty
        cur.execute("SELECT * FROM bag WHERE character_id = %s", (char_id,))
        bag = cur.fetchone()
        for i in range(1, 9):
            if bag[f"consumable_{i}_id"] is None or bag[f"consumable_{i}_id"] == item_id:
                return f"consumable_{i}_id"

    for i in range(1, 3 if item_type != 'consumable' else 9):
        col = f"{slot_prefix[item_type]}{i}_id"
        cur.execute(f"SELECT {col} FROM bag WHERE character_id = %s", (char_id,))
        row = cur.fetchone()
        if row[col] is None:
            return col
    return None

@app.route('/sell_item', methods=['POST'])
def sell_item():
    data = request.json
    char_id = data['char_id']
    item_type = data['item_type']
    item_id = data['item_id']
    slot_column = data['slot_column']

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    if item_type == 'consumable':
        sell_price = 5
    else:
        cur.execute(f"SELECT rarity FROM {item_type} WHERE {item_type[0]}_id = %s", (item_id,))
        rarity_row = cur.fetchone()
        rarity_to_price = {'Common': 10, 'Rare': 25, 'Epic': 50, 'Legend': 100}
        sell_price = rarity_to_price[rarity_row['rarity']]

    # Add gold
    cur.execute("SELECT gold FROM characters WHERE character_id = %s", (char_id,))
    gold = cur.fetchone()['gold'] + sell_price
    cur.execute("UPDATE characters SET gold = %s WHERE character_id = %s", (gold, char_id))

    # Remove from bag
    cur.execute(f"UPDATE bag SET {slot_column} = NULL WHERE character_id = %s", (char_id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"success": True, "gold": gold})

if __name__ == '__main__':
    app.run(debug=True)






def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='dnd_shop'
    )

