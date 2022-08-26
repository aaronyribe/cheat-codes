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
    data ={
        'id': session['user_id'],
    }
    return render_template("dashboard.html",user=User.get_by_id(data), games=Game.get_by_user_id(data) ) # TODO what should be shown on the dashboard??? shows=Show.get_all(),)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route("/create_game", methods=['GET','POST'])
def create_game():
    if request.method == "POST":
        if not Game.validate_edit(request.form):
            return redirect('/create_game')
        data ={ 
            "title": request.form['title'],
            "release_year": request.form['release_year'],
        }
        breakpoint()
        game = Game.save(data)
        return redirect('/dashboard')
    return render_template("create_game.html")

@app.route("/edit_game/<id>",methods=['GET','POST'])
def edit_game(id):
    if request.method == "GET":
        game = Game.get_by_id({'id': id})
        form = { 
            "title": request.form['title'],
            "release_year": request.form['release_year'],
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




