import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# ===== DATABASE CONFIGURATION =====
# Get database URL from environment variable (set in production)
# Fall back to SQLite for local development
database_url = os.environ.get('DATABASE_URL', 'sqlite:///game.db')

# Fix for Heroku's postgres:// vs postgresql://
# Some platforms use 'postgres://' but SQLAlchemy needs 'postgresql://'
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Add connection pool settings for production
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,           # Number of connections to keep
    'pool_recycle': 300,        # Recycle connections after 300 seconds
    'pool_pre_ping': True,      # Verify connections before using
}

# Initialize database
db = SQLAlchemy(app)

# ===== DATABASE MODEL =====
class GameRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_choice = db.Column(db.String(10), nullable=False)
    computer_choice = db.Column(db.String(10), nullable=False)
    result = db.Column(db.String(10), nullable=False)  # win, loss, tie
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_choice': self.user_choice,
            'computer_choice': self.computer_choice,
            'result': self.result,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

# ===== DATABASE INITIALIZATION =====
def init_db():
    """Create database tables if they don't exist"""
    with app.app_context():
        db.create_all()
        print(f"✅ Database initialized! Using: {database_url.split('@')[0].split('://')[0]} database")
        # Optional: Check if we can connect
        try:
            # Try a simple query to verify connection
            db.session.execute('SELECT 1')
            print("✅ Database connection successful!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")

# Call this when the app starts
init_db()

# ===== ROUTES =====
@app.route('/')
def index():
    return render_template('index.html')

# API: Save a game round (CREATE)
@app.route('/api/game', methods=['POST'])
def save_game():
    try:
        data = request.get_json()
        user_choice = data.get('user_choice')
        computer_choice = data.get('computer_choice')
        result = data.get('result')

        if not all([user_choice, computer_choice, result]):
            return jsonify({'error': 'Missing data'}), 400

        new_round = GameRound(
            user_choice=user_choice,
            computer_choice=computer_choice,
            result=result
        )
        db.session.add(new_round)
        db.session.commit()

        return jsonify({'message': 'Game round saved', 'id': new_round.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: Get all game history (READ)
@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        rounds = GameRound.query.order_by(GameRound.timestamp.desc()).all()
        return jsonify([r.to_dict() for r in rounds])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API: Get game statistics
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        total = GameRound.query.count()
        wins = GameRound.query.filter_by(result='win').count()
        losses = GameRound.query.filter_by(result='loss').count()
        ties = GameRound.query.filter_by(result='tie').count()
        return jsonify({
            'total': total,
            'wins': wins,
            'losses': losses,
            'ties': ties
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API: Delete a specific game round (DELETE)
@app.route('/api/game/<int:round_id>', methods=['DELETE'])
def delete_game(round_id):
    try:
        game_round = GameRound.query.get_or_404(round_id)
        db.session.delete(game_round)
        db.session.commit()
        return jsonify({'message': 'Game round deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: Delete all game history
@app.route('/api/history', methods=['DELETE'])
def delete_all_history():
    try:
        db.session.query(GameRound).delete()
        db.session.commit()
        return jsonify({'message': 'All history deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Health check endpoint (useful for deployment)
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)