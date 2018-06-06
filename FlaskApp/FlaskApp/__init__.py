from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content
from dbconnect import connection
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from functools import wraps




TOPIC_DICT = Content()

app = Flask(__name__)



@app.route('/')
def homepage():
    return render_template("main.html") 

@app.route('/dashboard/')
def dashboard():
    flash("flash test")
    flash("flash test 2")
    return render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT) 

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("log in")
            return redirect(url_for('loginPage'))
    return wrap

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You logged out")
    gc.collect()
    return redirect(url_for('homepage'))


@app.route('/login/', methods=['GET', 'POST'])
def loginPage():
    error = ""
    try: 
        c, conn = connection()
        if request.method == "POST":
            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                                (thwart(request.form['username']),))

            if int(data) == 0:
                error = "1Invalid credentials. Try Again."
                return render_template("login.html", error = error) 
            
            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'],data):
                session['logged_in']=True
                session['username'] = request.form['username']

                flash("You are now logged in")

                return redirect(url_for("dashboard"))

            else:
                error = "2Invalid credentials, Try again."

        gc.collect()

        return render_template("login.html", error = error) 
        
    except Exception as e:
        flash(e)
        error = "3Invalid credentials, try again."
        return render_template("login.html", error = error)  

    
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    acceptTOS = BooleanField('I accept the <a href="/tos/">Terms of Service</a> and <a href="/privacy/">Privacy Notice</a>', [validators.Required()])

@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username),))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)
            #Check this for PEAR
            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))
        



# Errors
@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404.html")

@app.errorhandler(405)
def methodNotFound(e):
    return render_template("405.html")



# @app.route('/sashboard/')
# def sashboard():
    # try:
        # return render_template("dashboard.html", TOPIC_DICT = DICT) 
    # except Exception as e:
        # return render_template("500.html", error = e) 

        

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'


    app.run()
