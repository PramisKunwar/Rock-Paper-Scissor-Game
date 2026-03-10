## 🪨📄✂️ Rock Paper Scissor Game with Flask Backend

A classic Rock Paper Scissor game built with HTML, CSS, JavaScript, and Flask. Features a backend that stores game history in a database with full CRUD functionality.

---

### ✨ Features
- Play Rock Paper Scissor against computer
- Real-time score tracking
- Game history with timestamps
- Delete individual games or all history
- Responsive design

---

### 🛠️ Built With
- HTML, CSS, JavaScript
- Flask (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL/SQLite database

---

### 🎮 Live Demo
[Play the game here](YOUR_VERCEL_RENDER_URL)

---

### 📸 Screenshots
![Game Screenshot](/static/Game%20SS.png)

---

### 🚀 Local Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python app.py`
6. Visit `http://127.0.0.1:5000`

---

### 🌐 Deployment
This app is deployed on [Vercel/Render/PythonAnywhere]. The live version uses PostgreSQL for data persistence.

---

### 📊 API Endpoints
- `GET /` - Game interface
- `POST /api/game` - Save game result
- `GET /api/history` - Get all games
- `GET /api/stats` - Get game statistics
- `DELETE /api/game/<id>` - Delete specific game
- `DELETE /api/history` - Delete all history

---