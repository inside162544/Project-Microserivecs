import os
from flask import Flask, jsonify, request, render_template
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


BOOKING_SERVICE_URL = "http://booking-service-url"

@app.route("/")
def index():
    return "Booking Service is up and running!"

@app.route("/", methods=["POST"])
def create_booking():
    try:
        # Get the booking data from the request
        data = request.json
        
        # Make a POST request to the Booking service
        response = requests.post(f"{BOOKING_SERVICE_URL}/bookings", json=data)
        
        # Check the response status code
        if response.status_code == 201:
            # Booking created successfully
            return jsonify({"message": "Booking created successfully", "booking_id": response.json()["id"]}), 201
        else:
            # Failed to create booking
            return jsonify({"error": "Failed to create booking"}), response.status_code
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

# Example endpoint to retrieve a single booking by ID
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

# Example endpoint to delete a booking by ID
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
    
@app.route("/", methods=["POST"])
def handle_booking_form():
    # ดำเนินการตามคำสั่งที่ต้องการ เช่น จัดการการจอง บันทึกข้อมูลลงในฐานข้อมูล เป็นต้น
    return "Booking form submitted successfully!"
if __name__ == "__main__":
    app.run(debug=True, port=5002)

