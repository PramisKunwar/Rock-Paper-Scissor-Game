import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# ===== DATABASE CONFIGURATION =====
database_url = os.environ.get('DATABASE_URL', 'sqlite:///game.db')

if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 300,
    'pool_pre_ping': True,
}

db = SQLAlchemy(app)

# ===== DATABASE MODEL =====
class GameRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_choice = db.Column(db.String(10), nullable=False)
    computer_choice = db.Column(db.String(10), nullable=False)
    result = db.Column(db.String(10), nullable=False)
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
    with app.app_context():
        db.create_all()
        print("✅ Database initialized!")

init_db()

# ===== ROUTES =====
@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        rounds = GameRound.query.order_by(GameRound.timestamp.desc()).all()
        return jsonify([r.to_dict() for r in rounds])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/history', methods=['DELETE'])
def delete_all_history():
    try:
        db.session.query(GameRound).delete()
        db.session.commit()
        return jsonify({'message': 'All history deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)