# Flask Socket.IO Chatroom

A real-time chatroom application built with Flask and Flask-SocketIO. Users can join predefined rooms, send messages, and see live user counts.

## Features

* **Server Connection Modal**: Prompt for server IP with reconnection logic (auto-reconnect attempts and timeouts).
* **Username Selection**: Modal to set and personalize display name before joining.
* **Multiple Predefined Chat Rooms**: `general`, `tech`, `sports`, `music`, `gaming`.
* **Real-Time Messaging**: Instant bidirectional communication via WebSockets using Flask-SocketIO.
* **Message History**: Previous messages are loaded for users when they join a room.
* **User Presence Tracking**: Live user counts per room, with dynamic updates as users join/leave.
* **System Notifications**: Broadcast messages when users enter or exit rooms.
* **Timestamps & Auto-Scroll**: Messages display formatted timestamps and the chat view auto-scrolls to newest message.

## Prerequisites

* Python 3.7 or higher
* `pip` package manager

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/pranjalpatil-23/Updated_Real_Time_Chat.git
   cd Updated_Real_Time_Chat
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **(If missing)** Generate `requirements.txt`

   ```bash
   pip install flask flask-socketio python-socketio python-engineio
   pip freeze > requirements.txt
   ```

## Configuration

Set a secret key for session management (optional):

```bash
export SECRET_KEY="your-secure-secret"
# Windows PowerShell:
$env:SECRET_KEY = "your-secure-secret"
```

## Running the Server

Start the Flask-SocketIO server:

```bash
python app.py
```

By default, the server listens on `0.0.0.0:5000`. Adjust in `app.py`:

```python
socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

## Client Usage

1. Connect to your server in a browser or with a Socket.IO client library:

   ```
   http://<server-address>:5000
   ```
2. Listen for events:

   * `room_list` – initial rooms and counts
   * `room_update` – updates to counts
   * `join_confirm` – confirmation after joining
   * `system_message` – user join/leave notifications
   * `receive_message` – incoming chat messages
3. Emit events to the server:

   * `join_room` with `{ room_name: "tech", username: "Alice" }`
   * `send_message` with `{ text: "Hello, world!" }`

## Project Structure

```
├── app.py            # Main Flask-SocketIO server
├── client.html       # Frontend UI and Socket.IO client script
├── requirements.txt  # Python dependency list
└── README.md         # Project documentation
```

## About

A simple demo app to illustrate real-time WebSocket communication with Flask.

## Resources

* [Client Code](client.html)
* [Server Code](app.py)

---
