from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# --- Utility Function ---
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='dungeons'
    )

# --- Routes ---

@app.route('/')
def home():
    return render_template('loxk.html')


@app.route('/create_character', methods=['POST'])
def create_character():
    data = request.get_json()
    name = data.get('name')
    race_id = data.get('race_id')
    class_id = data.get('class_id')
    description = data.get('description')

    if not all([name, race_id, class_id, description]):
        return jsonify({'message': 'Missing data'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert character
        cursor.execute("""
            INSERT INTO characters (name, race_id, class_id, description, level, strength, defense, intelligence, speed, luck, charisma)
            VALUES (%s, %s, %s, %s, 1, 0, 0, 0, 0, 0, 0)
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


@app.route('/get_races')
def get_races():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM races")
    races = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(races)


@app.route('/get_common_classes')
def get_common_classes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM classes WHERE class_type = 'Common'")
    classes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(classes)


@app.route('/get_characters')
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

if __name__ == '__main__':
    app.run(debug=True)
