Echo of Choices

## 🎮 Play the Game

[▶️ Play Meme TCG](https://echoes-of-the-mist.onrender.com/)

## ▶️ Run Locally
1. Clone this repository.
2. Open the project folder > app.py
3. Run: python app.py
   
Echo of Choices is a browser-based, choice-driven narrative game built with Python (Flask) on the backend and plain HTML/CSS/JavaScript on the frontend. The player reads through a story, makes choices at key moments, and those choices shape three underlying stats (Courage, Creativity, Risk) that determine how the story unfolds.

The project currently ships with a Thai-language horror/mystery story about a family moving to a strange new village, but the entire narrative engine is built to be story-agnostic — the code doesn't know or care what the story is about. This means the same engine can run any branching narrative, in any language, of any length, without touching the underlying application logic.

⭐ The Core Feature: Fully Flexible Story Editing (events.py)

The main selling point of this project is how easy it is to write, rewrite, extend, or completely replace the story without touching any other file.

All narrative content lives in a single file: events.py. It's a plain Python dictionary where each entry represents one "scene" (called an event) in the story:

python
EVENTS = {
    1: {
        'id': 1,
        'title': 'Scene title shown to the player',
        'text': 'The narrative text for this scene. Can be as long as you want.',
        'choices': [
            {
                'text': 'What this choice says on the button',
                'effects': {'courage': 0, 'creativity': 0, 'risk': 0},
                'next_event': 2   # which event id this choice leads to, or None to end the game
            },
            # add as many choices as you want, or just one for a linear "continue" scene
        ]
    },
    2: {
        # next scene...
    },
}

Because of this design:

Adding a new scene = adding a new numbered entry to the dictionary. No routing, HTML, or session code needs to change.
A scene can have 1 choice (a simple "Continue" button for pure storytelling) or many choices (a real branching decision point). The engine doesn't enforce a fixed number of choices per scene.
Branches can diverge and later reconverge — multiple choices can point to the same next_event, letting you offer meaningful-feeling decisions without having to write an exponentially growing number of unique scenes.
Stat effects are optional — set effects to all zeros for scenes that are purely narrative, and only apply real stat changes at the moments that matter to your design.
The whole story can be swapped out — delete everything in EVENTS and write an entirely different game, in any language, any tone, any length, and the rest of the application (Flask routes, templates, session handling) keeps working exactly as before.

In short: if you want to write or edit the game's story, events.py is the only file you need to open.

How the Rest of the Project Works (Brief Overview)
app.py — The Flask application. Defines the web routes (/, /start_game, /game, /make_choice, /ending, /restart) that tie the story data to the player's browser session.
game_logic.py — A small helper layer that fetches events by id and determines which ending text to show based on final stats.
player.py — A basic data structure representing a player's starting stats.
config.py — Application configuration (debug mode, session type, etc.).
templates/ — HTML pages rendered by Flask (via Jinja2):
base.html — shared layout and shared JavaScript helpers used by every page.
index.html — the start screen.
game.html — the main gameplay screen, rendering whichever event is currently active.
ending.html — the final screen, shown once a choice with next_event: None is reached.
static/ — CSS stylesheets for the different screens.
requirements.txt — Python dependencies (Flask, Werkzeug).
Running the Project
bash
pip install -r requirements.txt
python app.py




Player State

Player progress (current scene, accumulated stats, choice history) is stored in the Flask session (browser cookie) rather than a database, so no extra setup is required to play through a full story from start to finish.
