import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import requests

# Create a Flask application
app = Flask(__name__)

# Get the MongoDB password from the environment variable
mongodb_pw = os.getenv("MONGODB_PW")

# Construct the connection string
connection_string = f"mongodb+srv://inside162544:{mongodb_pw}@pythondb.piijqhq.mongodb.net/?retryWrites=true&w=majority&appName=PythonDB"

# Connect to MongoDB
client = MongoClient(connection_string)

# Connect to the database and collection
db = client["BookingDB"]
collection = db["BookingData"]

BOOKING_SERVICE_URL = "http://127.0.0.1:5002"

@app.route("/")
def index():
    return "Booking Service is running!"

@app.route("/bookings", methods=["POST"])
def create_booking():
    try:
        data = request.json
        booking = {
            "check_in_date": data['check_in_date'],
            "check_out_date": data['check_out_date'],
            "name": data['name'],
            "email": data['email'],
            "phone": data['phone'],
            "comments": data.get('comments', ''),
            "dormitory_id": data['dormitory_id']
        }

        result = collection.insert_one(booking)

        dormitory_id = data['dormitory_id']
        url = f"http://127.0.0.1:5001/dormitories/{dormitory_id}/decrement_room"
        dormitory_response = requests.post(url)

        if dormitory_response.status_code == 200:
            return jsonify({"message": "Booking created and room decremented successfully!"}), 201
        else:
            return jsonify({"error": "Booking created but failed to decrement room in dormitory service."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/bookings", methods=["GET"])
def get_bookings():
    try:
        # Retrieve all bookings from MongoDB
        bookings = list(collection.find({}))
        return jsonify(bookings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to retrieve a single booking by ID
@app.route("/bookings/<string:booking_id>", methods=["GET"])
def get_booking(booking_id):
    try:
        # Retrieve the booking by ID from MongoDB
        booking = collection.find_one({"_id": ObjectId(booking_id)})
        if booking:
            return jsonify(booking), 200
        else:
            return jsonify({"error": "Booking not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to delete a booking by ID
@app.route("/bookings/<string:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    try:
        # Delete the booking by ID from MongoDB
        result = collection.delete_one({"_id": ObjectId(booking_id)})
        if result.deleted_count == 1:
            return jsonify({"message": "Booking deleted successfully", "id": booking_id}), 200
        else:
            return jsonify({"error": "Booking not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)
