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
        "pw_hash": bcrypt.generate_password_hash(request.form['pw_hash'])
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
    if not bcrypt.check_password_hash(user.pw_hash, request.form['pw_hash']):
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
    return render_template("dashboard.html",user=User.get_by_id(data),  ) # TODO what should be shown on the dashboard??? shows=Show.get_all(),)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route("/create_show", methods=['GET','POST'])
def create_show():
    if request.method == "POST":
        if not Show.validate_edit(request.form):
            return redirect('/create_show')
        data ={ 
            "title": request.form['title'],
            "network": request.form['network'],
            "release_date": request.form['release_date'],
            "description": request.form['description'],
            "posted_by": session['user_id'],
        }
        show = Show.save(data)
        return redirect('/dashboard')
    return render_template("create_show.html")

@app.route("/edit_show/<id>",methods=['GET','POST'])
def edit_show(id):
    if request.method == "GET":
        show = Show.get_by_id({'id': id})
        form = { 
            "title": show.title,
            "network": show.network,
            "release_date": show.release_date,
            "description": show.description,
        }
    elif request.method == "POST":
        if not Show.validate_edit(request.form):
            return redirect(f'/edit_show{id}')
        data ={ 
            "id": id,
            "title": request.form['title'],
            "network": request.form['network'],
            "release_date": request.form['release_date'],
            "description": request.form['description'],
            "posted_by": session['user_id'],
        }
        show = Show.update(data)
        return redirect('/dashboard')
    return render_template("edit_show.html", form=form)


@app.route("/display_show/<id>")
def display_show(id):
    show = Show.get_by_id({'id': id})
    user = User.get_by_id({'id': show.posted_by})
    return render_template("display_show.html", show=show, posted_by=f'{user.first_name} {user.last_name}')

@app.route("/delete_show/<id>")
def delete_show(id):
    show = Show.delete_by_id({'id': id})
    return redirect('/dashboard')
