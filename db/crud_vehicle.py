import sqlite3

def insert_vehicle(model, mark, plate, type_vehicle, maximum_distance, delivery_person_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vehicle (model, mark, plate, type_vehicle, maximum_distance, delivery_person_id)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (model, mark, plate, type_vehicle, maximum_distance, delivery_person_id))
        conn.commit()

def get_all_vehicles():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicle;")
        return cursor.fetchall()

def get_vehicle_by_id(vehicle_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicle WHERE id = ?;", (vehicle_id,))
        return cursor.fetchone()

def update_vehicle(vehicle_id, model=None, mark=None, plate=None, type_vehicle=None, maximum_distance=None, delivery_person_id=None):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        fields, values = [], []

        if model:
            fields.append("model = ?")
            values.append(model)
        if mark:
            fields.append("mark = ?")
            values.append(mark)
        if plate:
            fields.append("plate = ?")
            values.append(plate)
        if type_vehicle:
            fields.append("type_vehicle = ?")
            values.append(type_vehicle)
        if maximum_distance:
            fields.append("maximum_distance = ?")
            values.append(maximum_distance)
        if delivery_person_id:
            fields.append("delivery_person_id = ?")
            values.append(delivery_person_id)

        if not fields:
            return

        values.append(vehicle_id)
        query = f"UPDATE vehicle SET {', '.join(fields)} WHERE id = ?;"
        cursor.execute(query, values)
        conn.commit()

def delete_vehicle(vehicle_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vehicle WHERE id = ?;", (vehicle_id,))
        conn.commit()
