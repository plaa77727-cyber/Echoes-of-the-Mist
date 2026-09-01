#run >> python app.py
from flask import Flask, render_template, request, session, jsonify, redirect
import secrets

from config import Config
from game_logic import GameLogic
from player import Player

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'echo-of-choices-dev-secret-2026'

game_logic = GameLogic()

# -------------------- HOME --------------------
@app.route('/')
def index():
    return render_template('index.html')


# -------------------- START GAME --------------------
@app.route('/start_game', methods=['POST'])
def start_game():
    player = Player()

    session.clear()
    session['player_courage'] = player.courage
    session['player_creativity'] = player.creativity
    session['player_risk'] = player.risk
    session['player_history'] = []
    session['current_event_id'] = 1

    return jsonify({
        'success': True,
        'redirect': '/game'
    })


# -------------------- GAME PAGE --------------------
@app.route('/game')
def game():
    if 'current_event_id' not in session:
        return redirect('/')

    event_id = session['current_event_id']
    event = game_logic.get_event(event_id)

    stats = {
        'courage': session.get('player_courage', 0),
        'creativity': session.get('player_creativity', 0),
        'risk': session.get('player_risk', 0)
    }

    return render_template('game.html', event=event, stats=stats)


# -------------------- MAKE CHOICE --------------------
@app.route('/make_choice', methods=['POST'])
def make_choice():
    data = request.get_json()
    choice_index = data.get('choice')

    if choice_index is None:
        return jsonify({'success': False, 'error': 'No choice sent'})

    event_id = session.get('current_event_id')
    if event_id is None:
        return jsonify({'success': False, 'error': 'No active game'})

    event = game_logic.get_event(event_id)
    choices = event.get('choices', [])

    if choice_index < 0 or choice_index >= len(choices):
        return jsonify({'success': False, 'error': 'Invalid choice'})

    choice = choices[choice_index]

    # Update stats
    session['player_courage'] = max(0, min(100, session['player_courage'] + choice['effects'].get('courage', 0)))
    session['player_creativity'] = max(0,
                                       min(100, session['player_creativity'] + choice['effects'].get('creativity', 0)))
    session['player_risk'] = max(0, min(100, session['player_risk'] + choice['effects'].get('risk', 0)))

    # Save history
    history = session.get('player_history', [])
    history.append({
        'event_id': event_id,
        'choice_index': choice_index,
        'choice_text': choice['text']
    })
    session['player_history'] = history

    # Next event
    next_event = choice.get('next_event')

    if next_event is None:
        return jsonify({
            'success': True,
            'game_over': True,
            'redirect': '/ending'
        })

    session['current_event_id'] = next_event

    return jsonify({
        'success': True,
        'game_over': False,
        'redirect': '/game'
    })


# -------------------- ENDING --------------------
@app.route('/ending')
def ending():
    stats = {
        'courage': session.get('player_courage', 0),
        'creativity': session.get('player_creativity', 0),
        'risk': session.get('player_risk', 0)
    }

    ending_text = game_logic.generate_ending(stats)

    return render_template('ending.html', stats=stats, ending=ending_text)


# -------------------- RESTART --------------------
@app.route('/restart', methods=['POST'])
def restart():
    session.clear()
    return jsonify({'success': True, 'redirect': '/'})


# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(debug=True)

#รันอันนี้ python app.py