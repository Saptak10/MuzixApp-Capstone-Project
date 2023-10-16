from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES
import datetime
import bson

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/muzixdb'  # Update with your MongoDB URI
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key
app.config['UPLOADED_IMAGES_DEST'] = 'uploads'  # Define the directory for uploaded images

mongo = PyMongo(app)
api = Api(app)
jwt = JWTManager(app)

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        # Check if the username already exists
        if mongo.db.users.find_one({'username': data['username']}):
            return {'message': 'Username already exists'}, 409
        # For example: mongo.db.users.insert(data)
        # Hash the user's password securely using bcrypt
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Check if an image was uploaded
        if 'image' in request.files:
            image = request.files['image']
            # Save the uploaded image using Flask-Uploads
            image_path = images.save(image, name=data['username'] + '.')
        else:
            image_path = None

        # Store user data with the hashed password in the database
        user_data = {
            'username': data['username'],
            'password': hashed_password,
            'profile_image': image_path
        }
        mongo.db.users.insert(user_data)
        return {'message': 'User registered successfully'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = mongo.db.users.find_one({'username': data['username']})

        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
            access_token = create_access_token(identity=data['username'])
            return {'access_token': access_token}, 200

        return {'message': 'Invalid username or password'}, 401

class UserProfile(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = mongo.db.users.find_one({'username': current_user}, {'_id': 0, 'password': 0})
        if user:
            return user, 200
        return {'message': 'User not found'}, 404

# Define a model for songs, assuming a collection called 'songs' in MongoDB
class SongModel:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.timestamp = datetime.datetime.now()

# Create a Flask-RESTful resource for managing songs
class SongsResource(Resource):
    # List all songs (Read operation)
    def get(self):
        songs = list(mongo.db.songs.find({}, {'_id': 0}).sort([("timestamp", -1)]))
        return jsonify({'songs': songs})

    # Add a new song (Create operation)
    @jwt_required
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()
        song = SongModel(data['title'], data['artist'], data['duration'])
        song_data = {
            'title': song.title,
            'artist': song.artist,
            'duration': song.duration,
            'timestamp': song.timestamp,
            'user_id': current_user,
        }
        mongo.db.songs.insert(song_data)
        return jsonify({'message': 'Song added successfully'})

# Create a Flask-RESTful resource for managing a single song
class SongResource(Resource):
    # Get a specific song by song_id (Read operation)
    def get(self, song_id):
        song = mongo.db.songs.find_one({'_id': bson.ObjectId(song_id)})
        if song:
            song.pop('_id', None)  # Remove MongoDB _id from the response
            return jsonify(song)
        return {'message': 'Song not found'}, 404

    # Update a specific song by song_id (Update operation)
    @jwt_required
    def put(self, song_id):
        data = request.get_json()
        current_user = get_jwt_identity()
        updated_song = {
            'title': data['title'],
            'artist': data['artist'],
            'duration': data['duration'],
            'user_id': current_user,
        }
        result = mongo.db.songs.update_one({'_id': bson.ObjectId(song_id), 'user_id': current_user},
                                           {'$set': updated_song})
        if result.modified_count > 0:
            return {'message': 'Song updated successfully'}
        return {'message': 'Song not found or not authorized to update'}, 404

    # Remove a specific song by song_id (Delete operation)
    @jwt_required
    def delete(self, song_id):
        current_user = get_jwt_identity()
        result = mongo.db.songs.delete_one({'_id': bson.ObjectId(song_id), 'user_id': current_user})
        if result.deleted_count > 0:
            return {'message': 'Song deleted successfully'}
        return {'message': 'Song not found or not authorized to delete'}, 404

# Add resources to the API
api.add_resource(SongsResource, '/api/v1/songs')
api.add_resource(SongResource, '/api/v1/songs/<string:song_id>')

api.add_resource(UserRegistration, '/api/v1/user/register')
api.add_resource(UserLogin, '/api/v1/user/login')
api.add_resource(UserProfile, '/api/v1/user/profile')

if __name__ == '__main__':
    app.run(debug=True)
