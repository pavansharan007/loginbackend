from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

# MongoDB Connection (Replace <your-uri>)
MONGO_URI = os.getenv("MONGO_URI", "your-mongodb-uri-here")
client = MongoClient(MONGO_URI)
db = client.smartinvest
users = db.users

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get("email")
    if users.find_one({"email": email}):
        return jsonify({"message": "Email already exists."}), 400

    user = {
        "fname": data.get("fname"),
        "mname": data.get("mname"),
        "lname": data.get("lname"),
        "dob": data.get("dob"),
        "email": email,
        "phone": data.get("phone"),
        "password": generate_password_hash(data.get("password")),
        "experience": data.get("experience")
    }

    users.insert_one(user)
    return jsonify({"message": "Signup successful."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid email or password."}), 401

    return jsonify({"message": "Login successful."}), 200

@app.route('/')
def home():
    return "SmartInvest Backend Running"

if __name__ == '__main__':
    app.run(debug=True)
