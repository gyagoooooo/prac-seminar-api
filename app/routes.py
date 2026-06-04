from flask import Blueprint, jsonify, request
from app.db import fetch_all, fetch_one, execute

api = Blueprint("api", __name__)


@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# -----------------------
# Rooms
# -----------------------

@api.route("/api/rooms", methods=["GET"])
def get_rooms():
    rows = fetch_all("""
        SELECT 
            id,
            name,
            capacity,
            equipment,
            DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS created_at,
            DATE_FORMAT(updated_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS updated_at
        FROM rooms
        ORDER BY id DESC
    """)

    return jsonify({
        "items": rows,
        "count": len(rows)
    })


@api.route("/api/rooms/<int:room_id>", methods=["GET"])
def get_room(room_id):
    row = fetch_one("""
        SELECT 
            id,
            name,
            capacity,
            equipment,
            DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS created_at,
            DATE_FORMAT(updated_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS updated_at
        FROM rooms
        WHERE id = %s
    """, (room_id,))

    if not row:
        return jsonify({"message": "room not found"}), 404

    return jsonify(row)


@api.route("/api/rooms", methods=["POST"])
def create_room():
    data = request.get_json() or {}

    name = data.get("name")
    capacity = data.get("capacity")
    equipment = data.get("equipment")

    if not name or not capacity:
        return jsonify({"message": "name and capacity are required"}), 400

    room_id = execute("""
        INSERT INTO rooms (name, capacity, equipment)
        VALUES (%s, %s, %s)
    """, (name, capacity, equipment))

    return jsonify({
        "id": room_id,
        "message": "created"
    }), 201


@api.route("/api/rooms/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    data = request.get_json() or {}

    room = fetch_one("""
        SELECT id
        FROM rooms
        WHERE id = %s
    """, (room_id,))

    if not room:
        return jsonify({"message": "room not found"}), 404

    name = data.get("name")
    capacity = data.get("capacity")
    equipment = data.get("equipment")

    if not name or not capacity:
        return jsonify({"message": "name and capacity are required"}), 400

    execute("""
        UPDATE rooms
        SET name = %s,
            capacity = %s,
            equipment = %s
        WHERE id = %s
    """, (name, capacity, equipment, room_id))

    return jsonify({
        "id": room_id,
        "message": "updated"
    })


@api.route("/api/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    room = fetch_one("""
        SELECT id
        FROM rooms
        WHERE id = %s
    """, (room_id,))

    if not room:
        return jsonify({"message": "room not found"}), 404

    execute("""
        DELETE FROM rooms
        WHERE id = %s
    """, (room_id,))

    return jsonify({
        "id": room_id,
        "message": "deleted"
    })


# -----------------------
# Reservations
# -----------------------

@api.route("/api/reservations", methods=["GET"])
def get_reservations():
    room_id = request.args.get("room_id")
    date = request.args.get("date")

    query = """
        SELECT 
            r.id,
            r.room_id,
            rm.name AS room_name,
            r.user_name,
            r.user_email,
            DATE_FORMAT(r.date, '%%Y-%%m-%%d') AS date,
            TIME_FORMAT(r.start_time, '%%H:%%i:%%s') AS start_time,
            TIME_FORMAT(r.end_time, '%%H:%%i:%%s') AS end_time,
            r.purpose,
            DATE_FORMAT(r.created_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS created_at,
            DATE_FORMAT(r.updated_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS updated_at
        FROM reservations r
        JOIN rooms rm ON r.room_id = rm.id
        WHERE 1 = 1
    """

    params = []

    if room_id:
        query += " AND r.room_id = %s"
        params.append(room_id)

    if date:
        query += " AND r.date = %s"
        params.append(date)

    query += " ORDER BY r.date DESC, r.start_time ASC"

    rows = fetch_all(query, tuple(params))

    return jsonify({
        "items": rows,
        "count": len(rows)
    })


@api.route("/api/reservations", methods=["POST"])
def create_reservation():
    data = request.get_json() or {}

    required_fields = [
        "room_id",
        "user_name",
        "user_email",
        "date",
        "start_time",
        "end_time"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    room = fetch_one("""
        SELECT id
        FROM rooms
        WHERE id = %s
    """, (data["room_id"],))

    if not room:
        return jsonify({"message": "room not found"}), 404

    duplicated = fetch_one("""
        SELECT id
        FROM reservations
        WHERE room_id = %s
          AND date = %s
          AND NOT (end_time <= %s OR start_time >= %s)
    """, (
        data["room_id"],
        data["date"],
        data["start_time"],
        data["end_time"]
    ))

    if duplicated:
        return jsonify({"message": "reservation time already exists"}), 409

    reservation_id = execute("""
        INSERT INTO reservations (
            room_id,
            user_name,
            user_email,
            date,
            start_time,
            end_time,
            purpose
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data["room_id"],
        data["user_name"],
        data["user_email"],
        data["date"],
        data["start_time"],
        data["end_time"],
        data.get("purpose")
    ))

    return jsonify({
        "id": reservation_id,
        "message": "reserved"
    }), 201


@api.route("/api/reservations/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    reservation = fetch_one("""
        SELECT id
        FROM reservations
        WHERE id = %s
    """, (reservation_id,))

    if not reservation:
        return jsonify({"message": "reservation not found"}), 404

    execute("""
        DELETE FROM reservations
        WHERE id = %s
    """, (reservation_id,))

    return jsonify({
        "id": reservation_id,
        "message": "cancelled"
    })
