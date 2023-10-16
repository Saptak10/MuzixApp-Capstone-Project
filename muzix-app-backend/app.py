from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
client = MongoClient('mongodb://localhost:27017')  # Replace with your MongoDB connection string

# Define the database and collection
db = client['song_db']
collection = db['songs']

# Create a route to get all customers
@app.route('/', methods=['GET'])
def get_all_songs():
    # songs = list(collection.find({}, {'_id': False}))
    # return jsonify(songs), 200
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)
