import os
import sqlite3
from flask import Flask
from flask import Flask, flash, request, redirect, url_for, render_template, session
from flask_session import Session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/assets/board_images'
UPLOAD_FOLDER_GAME = 'static/assets/game_pieces'
UPLOAD_FOLDER_DICE = 'static/assets/dice_sides'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "secret"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def home():
    con = sqlite3.connect('database.db')
    board_image_paths = ['assets/board_images/' + a[0]
                         for a in list(con.execute('''SELECT file_name FROM boards'''))]
    return render_template('home.html', boards=board_image_paths)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect("/")
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            db = sqlite3.connect('database.db')
            name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
            db.execute('''INSERT INTO boards (file_name) VALUES (?)''', (name,)
                       )  # current error: unique parameter failed (should return error html instead)
            db.commit()
            db.close()
            return redirect("/setup_board")

@app.route('/piece_uploader', methods=['GET', 'POST'])
def upload_pieces():
    if request.method == 'POST':
        # check if the post request has the file part
        currentIndex = 1
        currentFileKey = 'dice' + currentIndex
        while (currentFileKey in request.files):
            file = request.files[currentFileKey]
        return redirect("/setup_board")


@app.route('/select_image', methods=['GET', 'POST'])
def select_board():
    if request.method == "POST":
        session['board_path'] = request.form.get('selected-board')
        return redirect("/setup_board")

@app.route("/setup_board", methods=['GET', 'POST'])
def board_setup():
    return render_template('board_setup.html', board=session.get('board_path', None))

@app.route("/setup_finish", methods=['POST'])
def setup_finished():
    if request.method == 'POST':
        squares_length = int(request.form.get("maxSquareNumber"))
        square_coordinates_dict = {}
        for i in range(squares_length):
            coordinate_string = request.form.get(str(i))
            coordinates = coordinate_string.split(" ")
            square_coordinates_dict[str(i)] = (float(coordinates[0]), float(coordinates[1]))
        session['square_coordinates'] = square_coordinates_dict
        return redirect("/gamepiece")

@app.route("/gamepiece", methods=['GET', 'POST'])
def gamepiece_upload():
    return render_template('gamepiece_upload.html')

@app.route("/game", methods=['GET', 'POST'])
def play_game():
    if request.method == 'GET':
        return render_template('game.html', board=session.get('board_path', None), 
                                coordinates=session.get('square_coordinates', None), 
                                game_pieces=["assets/game_pieces/green_piece.png", "assets/game_pieces/blue_piece.png"], 
                                dice_sides=["assets/dice_sides/dice1.png", "assets/dice_sides/dice2.png", "assets/dice_sides/dice3.png", 
                                "assets/dice_sides/dice4.png", "assets/dice_sides/dice5.png", "assets/dice_sides/dice6.png"])

@app.route("/test", methods=['GET', 'POST'])
def test_website():
    return render_template('PixiJStest.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
