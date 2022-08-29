from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.cheat_code import CheatCode
from flask_app.models.game import Game
from flask_app.models.verified import Verified
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')


@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': session['user_id']}
    user=User.get_by_id(data)
    games=Game.get_by_user_id(data)
    game_data = {}
    if games:
        for game in games:
            codes_tried = 0
            cheat_codes = CheatCode.get_by_game_id({'game_id':game.id})
            if cheat_codes:
                for cheat_code in cheat_codes:
                    verified = Verified.get_by_cheat_code_id_user_id({'cheat_code_id': cheat_code.id, 'user_id': session['user_id']})
                    if verified and verified.verified != 0:
                        codes_tried += 1
            game_data[game.id] = {'game': game, 'total_cheats': len(cheat_codes) if cheat_codes else 0, 'tried': codes_tried}
    return render_template("dashboard.html",user=user, game_data=game_data)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route("/play_game", methods=['GET','POST'])
def play_game():
    if request.method == "POST":
        data ={ 
            "user_id": session['user_id'],
            "game_id": request.form['game_id'],
        }
        Game.play(data)
        return redirect('/dashboard')
    return render_template("play_game.html", games=Game.get_all())


@app.route("/unplay_game/<game_id>")
def unplay_game(id):
    game = Game.unplay({'user_id': session['user_id'], 'game_id': game_id})
    return redirect('/dashboard')


@app.route("/create_game", methods=['GET','POST'])
def create_game():
    if request.method == "POST":
        if not Game.validate_edit(request.form):
            return redirect('/create_game')
        data ={ 
            "title": request.form['title'],
            "release_year": request.form['release_year'],
            "posted_by": session['user_id'],
        }
        game = Game.save(data)
        return redirect('/play_game')
    return render_template("create_game.html")


@app.route("/edit_game/<id>",methods=['GET','POST'])
def edit_game(id):
    if request.method == "GET":
        game = Game.get_by_id({'id': id})
        form = { 
            "title": game.title,
            "release_year": game.release_year,
        }
    elif request.method == "POST":
        if not Game.validate_edit(request.form):
            return redirect(f'/edit_game{id}')
        data ={ 
            "id": id,
            "title": request.form['title'],
            "release_year": request.form['release_year'],
        }
        game = Game.update(data)
        return redirect('/dashboard')
    return render_template("edit_game.html", form=form)


@app.route("/display_game/<id>")
def display_game(id):
    game = Game.get_by_id({'id': id})
    user = User.get_by_id({'id': game.posted_by})
    return render_template("display_game.html", game=game, posted_by=f'{user.first_name} {user.last_name}')


@app.route("/delete_game/<id>")
def delete_game(id):
    game = Game.delete_by_id({'id': id})
    return redirect('/dashboard')


@app.route("/create_cheat/<game_id>", methods=['GET','POST'])
def create_cheat(game_id):
    if request.method == "POST":
        if not CheatCode.validate_edit(request.form):
            return redirect(f'/create_cheat/{game_id}')
        data ={ 
            "description": request.form['description'],
            "game_id": game_id,
            "submitted_by": session['user_id'],
        }
        cheat_code = CheatCode.save(data)
        return redirect(f"/show_cheats/{game_id}")
    return render_template("create_cheat.html", game=Game.get_by_id({'id':game_id}))


@app.route("/show_cheats/<game_id>")
def show_cheats(game_id):
    game = Game.get_by_id({'id': game_id})
    cheat_codes = CheatCode.get_by_game_id({'game_id': game_id})
    user = User.get_by_id({'id':session['user_id']})
    cheat_code_data = {}
    if cheat_codes:
        for cheat_code in cheat_codes:
            verified_by_user = Verified.get_by_cheat_code_id_user_id({'cheat_code_id': cheat_code.id, 'user_id': session['user_id']})
            if verified_by_user is not False:
                verified_by_user = verified_by_user.verified
            verifieds = Verified.get_by_cheat_code_id({'cheat_code_id': cheat_code.id})
            veri_score = 0
            for verified in verifieds:
                veri_score += verified.verified
            cheat_code_data[cheat_code.id] = {'cheat_code': cheat_code, 'veri_score': veri_score, 'verified_by_user': verified_by_user}
    return render_template("show_cheats.html", user=user, game=game, cheat_codes=cheat_codes, cheat_code_data=cheat_code_data)


@app.route("/edit_cheat/<cheat_id>",methods=['GET','POST'])
def edit_cheat(cheat_id):
    cheat_code = CheatCode.get_by_id({'id': cheat_id})
    game = Game.get_by_id({'id': cheat_code.game_id})
    if request.method == "GET":
        form = { 
            "description": cheat_code.description,
        }
    elif request.method == "POST":
        if not CheatCode.validate_edit(request.form):
            return redirect(f'/edit_cheat/{cheat_id}')
        data ={ 
            "id": cheat_id,
            "description": request.form['description'],
        }
        cheat_code = CheatCode.update(data)
        return redirect(f'/show_cheats/{game.id}')
    return render_template("edit_cheat.html", game=game, cheat_code=cheat_code, form=form)


@app.route("/delete_cheat/<cheat_id>")
def delete_cheat(cheat_id):
    game_id = CheatCode.get_by_id({'id': cheat_id}).game_id
    cheat = CheatCode.delete_by_id({'id': cheat_id})
    return redirect(f'/show_cheats/{game_id}')


@app.route("/cheat_yes/<cheat_id>")
def cheat_yes(cheat_id):
    verified = Verified.get_by_cheat_code_id_user_id({'cheat_code_id': cheat_id, 'user_id': session['user_id']})
    if verified:
        Verified.update({'id': verified.id, 'cheat_code_id': cheat_id, 'user_id': session['user_id'], 'verified': 1})
    else:
        Verified.save({'cheat_code_id': cheat_id, 'user_id': session['user_id'], 'verified': 1})
    return redirect(f'/show_cheats/{ CheatCode.get_by_id({"id": cheat_id}).game_id }')


@app.route("/cheat_no/<cheat_id>")
def cheat_no(cheat_id):
    verified = Verified.get_by_cheat_code_id_user_id({'cheat_code_id': cheat_id, 'user_id': session['user_id']})
    if verified:
        Verified.update({'id': verified.id, 'cheat_code_id': cheat_id, 'user_id': session['user_id'], 'verified': -1})
    else:
        Verified.save({'cheat_code_id': cheat_id, 'user_id': session['user_id'], 'verified': -1})
    return redirect(f'/show_cheats/{ CheatCode.get_by_id({"id": cheat_id}).game_id }')


@app.route("/not_tried/<cheat_id>")
def not_tried(cheat_id):
    verified = Verified.get_by_cheat_code_id_user_id({'cheat_code_id': cheat_id, 'user_id': session['user_id']})
    if verified:
        Verified.delete_by_id({'id': verified.id})
    return redirect(f'/show_cheats/{ CheatCode.get_by_id({"id": cheat_id}).game_id }')