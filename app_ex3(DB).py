from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField # Submit è un campo di testo che l'utente deve compilare
from wtforms.validators import DataRequired # DataRequired è un modo per validare se l'utente ha introdotto dei dati
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqplite:///user.db'

# secretKey
app.config['SECRET_KEY']= "Chiave segreta"


# initialize DB
db = SQLAlchemy(app)

# Create a Model of DB
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary_key is ID
    name = db.Column(db.String(100), nullable=False) #dentro string mettiamo un intero che è il max dei caratterri
    email= db.Column(db.String(120), nullable=False, unique=True) #ogni user può avere una mail unica
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #create A string representing
    def __repr__(self):
        return '<Name %r>' % self.name



# Create a Form class with
class NamerForm(FlaskForm):
    name=StringField("What's tupor name:", validators=[DataRequired()])
    submit=SubmitField("Submit")


# Create a Form class with
class UserForm(FlaskForm):
    name=StringField("Name:", validators=[DataRequired()])
    email=StringField("Email:", validators=[DataRequired()])
    submit=SubmitField("Submit")


# create route
# quando mettiamo ruote senza nulla siamo nella homepage
@app.route('/')
def index():  # put application's code here
    first_name="Klajdi"
    stuff="This is Bold Tex"

    esempio_lista = ["ex1", "ex3", "ex3"]
    return render_template("ex3/index.html", first_name= first_name,
                           stuff=stuff, esempio_lista=esempio_lista)


# localhost:5000 /user/esempi marco
@app.route('/user/<name>')
def user(name):
    return render_template("ex3/user.html", user_name= name)


# invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("ex3/404.html"), 404


# name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()

    if form.validate_on_submit():
        # se l'utente scrive qualcosa allora metti il valore nella variabile user_naem
        name = form.name.data
        form.name.data = ''

    return render_template("ex3/name.html", name=name,
                           form=form)

@app.route('/user/add', methods=['Get', 'Post'])
def add_user():
    name = None
    form = UserForm()

    if form.validate_on_submit():
        # Cerco nel DB se esiste un user con l'email corrente
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None: # se non esiste la creo con le info passate dall'utente
            user = Users(name=form.name.data, email=form.email.data)
            # Aggiunto l'utente al DB
            db.session.add(user)
            db.session.commit()

        name= form.name.data
        form.name.data=''
        form.email.data=''

        flash("User added successfully")

    our_user = Users.query.order_by(Users.date_added)
    return render_template("ex3/add_user.html", form=form, name= name)


if __name__ == '__main__':
    app.run()
