from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Folder, Flashcard
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'
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
    new_folder = Folder(
        name=data['name'],
        user_id=data['user_id']
    )
    db.session.add(new_folder)
    db.session.commit()

    return jsonify({
        "folder_id": new_folder.id,
        "message": "Folder created successfully"
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

@app.route('/folders/<int:folder_id>', methods=['DELETE'])
def delete_folder(folder_id):
    folder = Folder.query.get(folder_id)
    if not folder:
        return jsonify({"error": "Folder not found"}), 404

    db.session.delete(folder)
    db.session.commit()
    return jsonify({"message": "Folder deleted successfully"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)