from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()  # Fixed the typo in 'asc'
    message_list = [{'id': message.id, 'body': message.body, 'username': message.username, 'created_at': message.created_at.isoformat()} for message in messages]
    return jsonify(message_list), 200

@app.route('/messages', methods=['POST'])
def add_messages():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'id': new_message.id,'username':new_message.username, 'body': new_message.body, 'created_at': new_message.created_at.isoformat()}), 201  # Fixed the status code

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_messages(id):
    messaged = Message.query.get(id)
    if messaged:
        data = request.get_json()
        messaged.body = data.get('body')
        db.session.commit()
        return jsonify({'id': messaged.id, 'body': messaged.body, 'username': messaged.username, 'created_at': messaged.created_at.isoformat()}), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    messaged = Message.query.get(id)
    if messaged:
        db.session.delete(messaged)
        db.session.commit()
        return jsonify({'message': 'Message deleted'}), 200  # Fixed the response message

if __name__ == '__main__':
    app.run(port=5555)
