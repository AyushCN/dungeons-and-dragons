from flask import Flask, render_template, request, jsonify
import mysql.connector


dragon = Flask(__name__)


#----------------------------------routes-------------------------------------------------

@dragon.route('/')
def home():
    return render_template("/index.html")

@dragon.route('/view_characters')
def view_characters():
    return render_template("loxk.html")


@dragon.route('/rule')
def rules():
    return render_template("rules.html")

@dragon.route('/races')
def show_race_page():
    return render_template("race.html")

@dragon.route('/classes')
def classes_page():
    return render_template("classes.html")

@dragon.route('/start_adventure')
def start_adventure():
    return render_template("adventure.html")

@dragon.route("/shop")
def shop():
    char_id = request.args.get("char_id")
    return render_template("shop.html", character_id=char_id)


#------------------------------------------------------------------------------------------------------




@dragon.route("/get_characters")
def get_characters():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="dungeons"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            c.character_id,
            c.name,
            c.level,
            c.last_adventure,
            c.strength,
            c.defense,
            c.intelligence,
            c.speed,
            c.luck,
            c.charisma,

            r.race_name,
            r.race_str,
            r.race_def,
            r.race_int,
            r.race_spd,
            r.race_luck,
            r.race_cha,

            cl.class_name,
            cl.class_str,
            cl.class_def,
            cl.class_int,
            cl.class_spd,
            cl.class_luck,
            cl.class_cha,

            w1.w_name AS weapon_1_name,
            w1.w_str AS weapon_1_str,
            w1.w_int AS weapon_1_int,

            w2.w_name AS weapon_2_name,

            a1.a_name AS armor_1_name,
            a1.a_def AS armor_1_def,
            a1.a_spd AS armor_1_spd,

            a2.a_name AS armor_2_name,

            art1.art_name AS artifact_1_name,
            art1.art_luck AS artifact_1_luck,
            art1.art_cha AS artifact_1_cha,

            art2.art_name AS artifact_2_name,

            cons1.c_name AS consumable_1_name,
            b.consumable_1_count,
            cons2.c_name AS consumable_2_name,
            b.consumable_2_count,
            cons3.c_name AS consumable_3_name,
            b.consumable_3_count,
            cons4.c_name AS consumable_4_name,
            b.consumable_4_count,
            cons5.c_name AS consumable_5_name,
            b.consumable_5_count

        FROM characters c
        LEFT JOIN races r ON c.race_id = r.race_id
        LEFT JOIN classes cl ON c.class_id = cl.class_id
        LEFT JOIN bag b ON c.character_id = b.character_id
        LEFT JOIN weapon w1 ON b.w_1_id = w1.w_id
        LEFT JOIN weapon w2 ON b.w_2_id = w2.w_id
        LEFT JOIN armor a1 ON b.a_1_id = a1.a_id
        LEFT JOIN armor a2 ON b.a_2_id = a2.a_id
        LEFT JOIN artifact art1 ON b.art_1_id = art1.art_id
        LEFT JOIN artifact art2 ON b.art_2_id = art2.art_id
        LEFT JOIN consumable cons1 ON b.consumable_1_id = cons1.c_id
        LEFT JOIN consumable cons2 ON b.consumable_2_id = cons2.c_id
        LEFT JOIN consumable cons3 ON b.consumable_3_id = cons3.c_id
        LEFT JOIN consumable cons4 ON b.consumable_4_id = cons4.c_id
        LEFT JOIN consumable cons5 ON b.consumable_5_id = cons5.c_id
    """)

    characters = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(characters)
#------------------------------------------------------------------------------------------
@dragon.route('/get_races')
def get_races():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="password",  # Replace with your MySQL password
        database="dungeons"  # Replace with your database name
    )
    cursor = conn.cursor(dictionary=True)

    # Query to retrieve all races from the database
    cursor.execute("""
        SELECT race_id,race_name, race_type, race_description,
               race_str, race_def, race_int, race_spd, race_luck, race_cha,
               passive_trait, negative_trait, active_skill
        FROM races
    """)

    # Fetch all results
    races = cursor.fetchall()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

    # Return the results as JSON
    return jsonify(races)

#----------------------------------------------------------------------------------------

@dragon.route('/get_classes')
def get_classes():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="password",  # Replace with your MySQL password
        database="dungeons"  # Replace with your database name
    )
    cursor = conn.cursor(dictionary=True)

    # Query to retrieve all classes from the database
    cursor.execute("""
        SELECT class_id,class_name, class_type, class_description,
               class_str, class_def, class_int, class_spd, class_luck, class_cha
        FROM classes
    """)

    # Fetch all results
    classes = cursor.fetchall()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

    # Return the results as JSON
    return jsonify(classes)

#------------------------------------------------------------------------------------------

@dragon.route('/get_common_classes')
def get_common_classes():
    # Establish connection to the MySQL database
    conn = mysql.connector.connect(host="localhost", user="root", password="password", database="dungeons")
    cursor = conn.cursor(dictionary=True)

    # SQL query to retrieve only 'Common' class data
    cursor.execute("SELECT class_id,class_name, class_type, class_description, "
                   "class_str, class_def, class_int, class_spd, class_luck, class_cha "
                   "FROM classes WHERE class_type = 'Common'")
    
    # Fetch all rows from the query
    common_classes = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Return the result as JSON to the frontend
    return jsonify(common_classes)
#----------------------------------------------------------------------------------------



@dragon.route('/create_character', methods=['POST'])
def create_character():
    data = request.get_json()
    name = data.get('name')
    race_id = data.get('race_id')
    class_id = data.get('class_id')
    description = data.get('description')

    if not all([name, race_id, class_id, description]):
        return jsonify({'message': 'Missing data'}), 400

    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="password",  # Replace with your MySQL password
        database="dungeons"  # Replace with your database name
    )
    cursor = conn.cursor()

    try:
        # Insert character
        cursor.execute("""
            INSERT INTO characters (name, race_id, class_id, description, level)
            VALUES (%s, %s, %s, %s, 1)
        """, (name, race_id, class_id, description))
        conn.commit()

        character_id = cursor.lastrowid

        # Create starter bag
        cursor.execute("INSERT INTO bag (character_id) VALUES (%s)", (character_id,))
        conn.commit()

        # Fetch character for confirmation
        cursor.execute("SELECT * FROM characters WHERE character_id = %s", (character_id,))
        character = cursor.fetchone()

        return jsonify()

    except Exception as e:
        print('Error:', e)
        return jsonify({'message': 'Error creating character.'}), 500

    finally:
        cursor.close()
        conn.close()



#------------------------------------------------------------------------------------------
@dragon.route("/get_character_details")
def get_character_details():
    # Retrieve the character ID from the query parameters
    char_id = request.args.get("char_id")

    # Check if character ID is provided
    if not char_id:
        return jsonify({"error": "Character ID is missing"}), 400

    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="password",  # Replace with your MySQL password
            database="dungeons"  # Replace with your database name
        )

        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)

            # Query to fetch character details
            query = """
            SELECT
                c.character_id,
                c.name,
                c.level,
                c.last_adventure,
                strength,
                defense,
                intelligence,
                speed,
                luck,
                charisma,
                gold,
                r.race_name,
                r.race_str,
                r.race_def,
                r.race_int,
                r.race_spd,
                r.race_luck,
                r.race_cha,
                cl.class_name,
                cl.class_str,
                cl.class_def,
                cl.class_int,
                cl.class_spd,
                cl.class_luck,
                cl.class_cha,
                w1.w_name AS weapon_1_name,
                w1.w_str AS weapon_1_str,
                w1.w_int AS weapon_1_int,
                w2.w_name AS weapon_2_name,
                a1.a_name AS armor_1_name,
                a1.a_def AS armor_1_def,
                a1.a_spd AS armor_1_spd,
                a2.a_name AS armor_2_name,
                art1.art_name AS artifact_1_name,
                art1.art_luck AS artifact_1_luck,
                art1.art_cha AS artifact_1_cha,
                art2.art_name AS artifact_2_name,
                art2.art_cha AS artifact_2_cha,
                -- Consumable items
                cons1.c_name AS consumable_1_name,
                b.consumable_1_count,
                cons2.c_name AS consumable_2_name,
                b.consumable_2_count,
                cons3.c_name AS consumable_3_name,
                b.consumable_3_count,
                cons4.c_name AS consumable_4_name,
                b.consumable_4_count,
                cons5.c_name AS consumable_5_name,
                b.consumable_5_count,
                cons6.c_name AS consumable_6_name,
                b.consumable_6_count,
                cons7.c_name AS consumable_7_name,
                b.consumable_7_count,
                cons8.c_name AS consumable_8_name,
                b.consumable_8_count
            FROM characters c
            LEFT JOIN races r ON c.race_id = r.race_id
            LEFT JOIN classes cl ON c.class_id = cl.class_id
            LEFT JOIN bag b ON c.character_id = b.character_id
            LEFT JOIN weapon w1 ON b.w_1_id = w1.w_id
            LEFT JOIN weapon w2 ON b.w_2_id = w2.w_id
            LEFT JOIN armor a1 ON b.a_1_id = a1.a_id
            LEFT JOIN armor a2 ON b.a_2_id = a2.a_id
            LEFT JOIN artifact art1 ON b.art_1_id = art1.art_id
            LEFT JOIN artifact art2 ON b.art_2_id = art2.art_id
            LEFT JOIN consumable cons1 ON b.consumable_1_id = cons1.c_id
            LEFT JOIN consumable cons2 ON b.consumable_2_id = cons2.c_id
            LEFT JOIN consumable cons3 ON b.consumable_3_id = cons3.c_id
            LEFT JOIN consumable cons4 ON b.consumable_4_id = cons4.c_id
            LEFT JOIN consumable cons5 ON b.consumable_5_id = cons5.c_id
            LEFT JOIN consumable cons6 ON b.consumable_6_id = cons6.c_id
            LEFT JOIN consumable cons7 ON b.consumable_7_id = cons7.c_id
            LEFT JOIN consumable cons8 ON b.consumable_8_id = cons8.c_id
            WHERE c.character_id = %s;
            """

            # Execute the query with the character ID
            cursor.execute(query, (char_id,))
            character = cursor.fetchone()

            # If no character found, return an error
            if not character:
                return jsonify({"error": "Character not found"}), 404

            # Prepare the response data
            data = {
                "character_id": character["character_id"],
                "name": character["name"],
                "level": character["level"],
                "last_adventure": character["last_adventure"],
                "gold": character["gold"],
                "race_name": character["race_name"],
                "class_name": character["class_name"],
                "strength": character["strength"],
                "defense": character["defense"],
                "intelligence": character["intelligence"],
                "speed": character["speed"],
                "luck": character["luck"],
                "charisma": character["charisma"],
                "race_str": character["race_str"],
                "race_def": character["race_def"],
                "race_int": character["race_int"],
                "race_spd": character["race_spd"],
                "race_luck": character["race_luck"],
                "race_cha": character["race_cha"],
                "class_str": character["class_str"],
                "class_def": character["class_def"],
                "class_int": character["class_int"],
                "class_spd": character["class_spd"],
                "class_luck": character["class_luck"],
                "class_cha": character["class_cha"],
                "weapon_1_name": character["weapon_1_name"],
                "weapon_2_name": character["weapon_2_name"],
                "weapon_1_str": character["weapon_1_str"],
                "weapon_1_int": character["weapon_1_int"],
                "armor_1_name": character["armor_1_name"],
                "armor_2_name": character["armor_2_name"],
                "armor_1_def": character["armor_1_def"],
                "armor_1_spd": character["armor_1_spd"],
                "artifact_1_name": character["artifact_1_name"],
                "artifact_2_name": character["artifact_2_name"],
                "artifact_1_luck": character["artifact_1_luck"],
                "artifact_1_cha": character["artifact_1_cha"],
                "artifact_2_cha": character["artifact_2_cha"],
                "consumable_1_name": character["consumable_1_name"],
                "consumable_1_count": character["consumable_1_count"],
                "consumable_2_name": character["consumable_2_name"],
                "consumable_2_count": character["consumable_2_count"],
                "consumable_3_name": character["consumable_3_name"],
                "consumable_3_count": character["consumable_3_count"],
                "consumable_4_name": character["consumable_4_name"],
                "consumable_4_count": character["consumable_4_count"],
                "consumable_5_name": character["consumable_5_name"],
                "consumable_5_count": character["consumable_5_count"],
                "final_stats": {
                    "str": (character["strength"] or 0) + (character["race_str"] or 0) + (character["class_str"] or 0) + (character["weapon_1_str"] or 0),
                    "def": (character["defense"] or 0) + (character["race_def"] or 0) + (character["class_def"] or 0) + (character["armor_1_def"] or 0),
                    "int": (character["intelligence"] or 0) + (character["race_int"] or 0) + (character["class_int"] or 0) + (character["weapon_1_int"] or 0),
                    "spd": (character["speed"] or 0) + (character["race_spd"] or 0) + (character["class_spd"] or 0) + (character["armor_1_spd"] or 0),
                    "luck": (character["luck"] or 0) + (character["race_luck"] or 0) + (character["class_luck"] or 0) + (character["artifact_1_luck"] or 0),
                    "cha": (character["charisma"] or 0) + (character["race_cha"] or 0) + (character["class_cha"] or 0) + (character["artifact_2_cha"] or 0),
                }
            }

            # Close the cursor and the connection
            cursor.close()
            conn.close()

            # Return the response data as JSON
            return jsonify(data)

    except Error as e:
        # Return an error if database operation fails
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        # Return a generic error for unexpected issues
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

#--------------------------------------------------------------------------------------------


@dragon.route('/api/items', methods=['GET'])
def get_items():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="dungeons"
    )
    cursor = connection.cursor()

    # Weapons
    cursor.execute("SELECT w_id, w_name, rarity, w_str, w_int, special_effects, weapon_description FROM weapon")
    weapons = cursor.fetchall()
    weapon_list = [{
        "id": w[0],
        "name": w[1],
        "rarity": w[2],
        "str": w[3],
        "int": w[4],
        "effects": eval(w[5]) if isinstance(w[5], str) else [],
        "desc": w[6]
    } for w in weapons]

    # Armor
    cursor.execute("SELECT a_id, a_name, rarity, a_def, a_spd, special_effects, armor_description FROM armor")
    armor = cursor.fetchall()
    armor_list = [{
        "id": a[0],
        "name": a[1],
        "rarity": a[2],
        "def": a[3],
        "spd": a[4],
        "effects": eval(a[5]) if isinstance(a[5], str) else [],
        "desc": a[6]
    } for a in armor]

    # Artifacts
    cursor.execute("SELECT art_id, art_name, rarity, art_luck, art_cha, special_effects, art_description FROM artifact")
    artifacts = cursor.fetchall()
    artifact_list = [{
        "id": art[0],
        "name": art[1],
        "rarity": art[2],
        "luck": art[3],
        "cha": art[4],
        "effects": eval(art[5]) if isinstance(art[5], str) else [],
        "desc": art[6]
    } for art in artifacts]

    # Consumables
    cursor.execute("SELECT c_id, c_name, rarity, effect, price, description FROM consumable")
    consumables = cursor.fetchall()
    consumable_list = [{
        "id": c[0],
        "name": c[1],
        "rarity": c[2],
        "effects": eval(c[3]) if isinstance(c[3], str) else [],
        "price": c[4],
        "desc": c[5]
    } for c in consumables]

    connection.close()

    # Return items as properly structured JSON
    return jsonify({
        'weapons': weapon_list,
        'armor': armor_list,
        'artifacts': artifact_list,
        'consumables': consumable_list
    })

#---------------------------------------------------------------------------------------------


@dragon.route("/buy_item", methods=["POST"])
def buy_item():
    # Extract data from the request
    char_id = request.json.get("char_id")
    item_id = request.json.get("item_id")
    item_type = request.json.get("item_type")  # Weapon, Armor, Consumable, etc.
    item_price = request.json.get("item_price")  # Price of the item

    # Validate input
    if not char_id or not item_id or not item_price or not item_type:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="dungeons"
        )

        if conn.is_connected():
            cursor = conn.cursor()

            # Query to get the current gold of the character
            cursor.execute("SELECT gold FROM characters WHERE character_id = %s", (char_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": "Character not found"}), 404

            current_gold = result[0]

            # Check if the character has enough gold
            if current_gold < item_price:
                return jsonify({"error": "Not enough gold"}), 400

            # Deduct the gold
            new_gold = current_gold - item_price
            cursor.execute("UPDATE characters SET gold = %s WHERE character_id = %s", (new_gold, char_id))

            # Add the item to the character's inventory based on item type
            if item_type == "weapon":
                cursor.execute("INSERT INTO bag (character_id, w_1_id) VALUES (%s, %s)", (char_id, item_id))
            elif item_type == "armor":
                cursor.execute("INSERT INTO bag (character_id, a_1_id) VALUES (%s, %s)", (char_id, item_id))
            elif item_type == "consumable":
                cursor.execute("INSERT INTO bag (character_id, consumable_1_id) VALUES (%s, %s)", (char_id, item_id))
            else:
                return jsonify({"error": "Invalid item type"}), 400

            # Commit the transaction
            conn.commit()

            # Close the cursor and the connection
            cursor.close()
            conn.close()

            return jsonify({"message": "Item purchased successfully", "new_gold": new_gold})

    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

#---------------------------------------------------------------------------------------------

@dragon.route("/sell_item", methods=["POST"])
def sell_item():
    # Extract data from the request
    char_id = request.json.get("char_id")
    item_id = request.json.get("item_id")
    item_type = request.json.get("item_type")  # Weapon, Armor, Consumable, etc.
    item_price = request.json.get("item_price")  # Price of the item

    # Validate input
    if not char_id or not item_id or not item_price or not item_type:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="dungeons"
        )

        if conn.is_connected():
            cursor = conn.cursor()

            # Query to get the current gold of the character
            cursor.execute("SELECT gold FROM characters WHERE character_id = %s", (char_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": "Character not found"}), 404

            current_gold = result[0]

            # Add the gold
            new_gold = current_gold + item_price
            cursor.execute("UPDATE characters SET gold = %s WHERE character_id = %s", (new_gold, char_id))

            # Remove the item from the character's inventory based on item type
            if item_type == "weapon":
                cursor.execute("UPDATE bag SET w_1_id = NULL WHERE character_id = %s AND w_1_id = %s", (char_id, item_id))
            elif item_type == "armor":
                cursor.execute("UPDATE bag SET a_1_id = NULL WHERE character_id = %s AND a_1_id = %s", (char_id, item_id))
            elif item_type == "consumable":
                cursor.execute("UPDATE bag SET consumable_1_id = NULL WHERE character_id = %s AND consumable_1_id = %s", (char_id, item_id))
            else:
                return jsonify({"error": "Invalid item type"}), 400

            # Commit the transaction
            conn.commit()

            # Close the cursor and the connection
            cursor.close()
            conn.close()

            return jsonify({"message": "Item sold successfully", "new_gold": new_gold})

    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

#---------------------------------------------------------------------------------------------
@dragon.route('/get_weapons')
def get_weapons():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Your MySQL username
        password="password",  # Your MySQL password
        database="dungeons"  # Your database name
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM weapon")
    weapons = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(weapons)


@dragon.route('/get_armor')
def get_armor():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Your MySQL username
        password="password",  # Your MySQL password
        database="dungeons"  # Your database name
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM armor")
    armor = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(armor)


@dragon.route('/get_artifacts')
def get_artifacts():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Your MySQL username
        password="password",  # Your MySQL password
        database="dungeons"  # Your database name
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM artifact")
    artifacts = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(artifacts)


@dragon.route('/get_consumables')
def get_consumables():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Your MySQL username
        password="password",  # Your MySQL password
        database="dungeons"  # Your database name
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM consumable")
    consumables = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(consumables)

#---------------------------------------------------------------------------------------------
@dragon.route('/shop_data', methods=['GET'])
def shop_data():
    weapons = get_weapons()  # Fetch from DB
    armor = get_armor()      # Fetch from DB
    artifacts = get_artifacts()  # Fetch from DB
    consumables = get_consumables()  # Fetch from DB
    return jsonify({
        'weapons': weapons,
        'armor': armor,
        'artifacts': artifacts,
        'consumables': consumables
    })

#---------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

if __name__ == '__main__':
    dragon.run(debug=True, host="0.0.0.0", port=5000)
