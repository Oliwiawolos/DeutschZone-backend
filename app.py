import time
import psycopg2
import os

max_retries = 10
while max_retries > 0:
    try:
        conn = psycopg2.connect(os.environ['SQLALCHEMY_DATABASE_URI'])
        conn.close()
        print("✅ DB is ready!")
        break
    except psycopg2.OperationalError:
        print("⏳ Waiting for the database to be ready...")
        time.sleep(3)
        max_retries -= 1

from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Folder, Flashcard, User
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
@app.route('/')
def home():
    return jsonify({"message":"Flask API is running"})


@app.route('/flashcards', methods=['POST'])
def create_flashcard():
    data = request.json
    new_card = Flashcard(
        term=data['term'],
        definition=data['definition'],
        folder_id=data['folder_id']
    )

    db.session.add(new_card)
    db.session.commit()
    return jsonify({"message": "Flashcard added"})

@app.route ('/folders/<int:user_id>', methods=['GET'])
def get_folder(user_id):
    folder = Folder.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": f.id, "name": f.name} for f in folder])

@app.route('/folders', methods=['POST'])
def create_folder():
    data = request.get_json()

    flashcards_data = data.get('flashcards', [])

    valid_flashcards = [fc for fc in flashcards_data if fc.get('term') and fc.get('definition')]
    if len(valid_flashcards) < 2:
        return jsonify({"error": "You must add at least 2 flashcards."}), 400

    new_folder = Folder(
        name=data['name'],
        user_id=data['user_id']
    )
    db.session.add(new_folder)
    db.session.flush()

    for fc in valid_flashcards:
        flashcard = Flashcard(
            term=fc['term'],
            definition=fc['definition'],
            folder_id=new_folder.id
        )
        db.session.add(flashcard)

    db.session.commit()

    return jsonify({
        "folder_id": new_folder.id,
        "message": "Folder and flashcards created successfully"
    }), 201

@app.route('/flashcards/<int:folder_id>', methods=['GET'])
def get_flashcard(folder_id):
    flashcards=Flashcard.query.filter_by(folder_id=folder_id).all()
    return jsonify([{"id":f.id, "term": f.term, "definition": f.definition} for f in flashcards])

@app.route('/flashcards/<int:flashcard_id>', methods=['DELETE'])
def delete_flashcard(flashcard_id):
    flashcard=Flashcard.query.get(flashcard_id)
    if flashcard:
        db.session.delete(flashcard)
        db.session.commit()
        return jsonify({"message":"Flashcard deleted"})
    return jsonify({"error":"Flashcard not found"}), 404

@app.route('/flashcards/<int:flashcard_id>', methods=['PUT'])
def update_flashcard(flashcard_id):
    flashcard = Flashcard.query.get(flashcard_id)
    if not flashcard:
        return jsonify({"error": "Flashcard not found"}), 404

    data = request.json
    flashcard.term = data['term']
    flashcard.definition = data['definition']

    db.session.commit()
    return jsonify({"message": "Flashcard updated successfully"})

@app.route('/folder/<int:folder_id>', methods=['PUT'])
def update_folder_name(folder_id):
    folder = Folder.query.get(folder_id)
    if not folder:
        return jsonify({"error": "Folder not found"}), 404

    data = request.get_json()
    folder.name = data.get('name', folder.name)
    db.session.commit()

    return jsonify({"message": "Folder name updated successfully"})
@app.route('/folder/<int:folder_id>', methods=['GET'])
def get_folder_name(folder_id):
    folder = Folder.query.get(folder_id)
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    return jsonify({"id": folder.id, "name": folder.name})

@app.route('/folders/<int:folder_id>', methods=['DELETE'])
def delete_folder(folder_id):
    folder = Folder.query.get(folder_id)
    if not folder:
        return jsonify({"error": "Folder not found"}), 404

    db.session.delete(folder)
    db.session.commit()
    return jsonify({"message": "Folder deleted successfully"})

@app.route('/sync-user', methods=['POST'])
def sync_user():
    data = request.get_json()
    email = data['email']
    firebase_uid = data['firebase_uid']

    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        new_user = User(email=email, password='firebase')
        db.session.add(new_user)
        db.session.commit()

    return jsonify({"message": "User synced successfully"})
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
