from flask import Flask, send_file, request  # Added request here
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# ... rest of your server code remains the same ...

# Predefined rooms with message history
PREDEFINED_ROOMS = ['general', 'tech', 'sports', 'music', 'gaming']
room_users = defaultdict(set)  # {room_name: set(session_ids)}
user_info = {}  # {session_id: {'room': room_name, 'name': username}}
message_history = defaultdict(list)  # {room_name: [messages]}

@app.route('/')
def serve_client():
    return send_file('client.html')

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    emit('room_list', get_room_status())

@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    if session_id in user_info:
        room_name = user_info[session_id]['room']
        username = user_info[session_id]['name']
        room_users[room_name].discard(session_id)
        del user_info[session_id]
        update_room_status()
        emit('system_message', {
            'text': f'{username} has left the room',
            'timestamp': datetime.now().isoformat()
        }, room=room_name)
    print(f'Client disconnected: {session_id}')

@socketio.on('join_room')
def handle_join_room(data):
    session_id = request.sid
    room_name = data['room_name']
    username = data.get('username', 'Anonymous')
    
    if room_name not in PREDEFINED_ROOMS:
        emit('error', {'message': 'Invalid room name'})
        return
    
    # Leave previous room
    if session_id in user_info:
        previous_room = user_info[session_id]['room']
        leave_room(previous_room)
        room_users[previous_room].discard(session_id)
    
    # Join new room
    join_room(room_name)
    user_info[session_id] = {
        'room': room_name,
        'name': username
    }
    room_users[room_name].add(session_id)
    
    # Send message history to new user
    for msg in message_history[room_name]:
        emit('receive_message', msg, room=session_id)
    
    update_room_status()
    emit('system_message', {
        'text': f'{username} has joined the room',
        'timestamp': datetime.now().isoformat()
    }, room=room_name)

@socketio.on('send_message')
def handle_send_message(data):
    session_id = request.sid
    if session_id not in user_info:
        return
    
    user_data = user_info[session_id]
    message = {
        'sender': user_data['name'],
        'text': data['text'],
        'timestamp': datetime.now().isoformat(),
        'room': user_data['room']
    }
    
    message_history[user_data['room']].append(message)
    emit('receive_message', message, room=user_data['room'])

def update_room_status():
    status = get_room_status()
    emit('room_update', status, broadcast=True)

def get_room_status():
    return {
        room: {
            'count': len(users),
            'name': room
        }
        for room in PREDEFINED_ROOMS
        for users in [room_users[room]]
    }

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)