from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField # Submit è un campo di testo che l'utente deve compilare
from wtforms.validators import DataRequired # DataRequired è un modo per validare se l'utente ha introdotto dei dati


app = Flask(__name__)
app.config['SECRET_KEY']= "Chiave segreta"


# Create a Form class with
class NamerForm(FlaskForm):
    name=StringField("What's tupor name:", validators=[DataRequired()])
    submit=SubmitField("Submit")


# create route
# quando mettiamo ruote senza nulla siamo nella homepage
@app.route('/')
def index():  # put application's code here
    first_name="Klajdi"
    stuff="This is Bold Tex"

    esempio_lista = ["ex1", "ex2", "ex3"]
    return render_template("ex2/index.html", first_name= first_name,
                           stuff=stuff, esempio_lista=esempio_lista)


# localhost:5000 /user/esempi marco
@app.route('/user/<name>')
def user(name):
    return render_template("ex2/user.html", user_name= name)


# invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("ex2/404.html"), 404


# name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()

    if form.validate_on_submit():
        # se l'utente scrive qualcosa allora metti il valore nella variabile user_naem
        name = form.name.data
        form.name.data = ''

    return render_template("ex2/name.html", name=name,
                           form=form)


if __name__ == '__main__':
    app.run()
