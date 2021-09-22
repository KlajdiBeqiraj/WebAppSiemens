import numpy as np
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField # Submit è un campo di testo che l'utente deve compilare
from wtforms.validators import DataRequired # DataRequired è un modo per validare se l'utente ha introdotto dei dati
import pandas as pd
import plotly
import plotly.express as px
import json
import plotly.graph_objs as go


app = Flask(__name__)
app.config['SECRET_KEY']= "Chiave segreta"

def create_plot():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


# Create a Form class with
class NamerForm(FlaskForm):
    name=StringField("What's tupor name:", validators=[DataRequired()])
    submit=SubmitField("Submit")


# create route
# quando mettiamo ruote senza nulla siamo nella homepage
@app.route('/')
def index():  # put application's code here
    bar = create_plot()
    # return render_template("AdobeHTML/ModelWeb/SaasHome.html", plot=bar)
    # return render_template("AdobeHTML/ModelWeb2/Minimal_Dashboard_Challenge.html", plot=bar)
    return render_template("AdobeHTML/ModelWeb3/Dashboard___ProManage___Dark_Theme.html", plot=bar)
    # return render_template("AdobeHTML/ModelWeb4/dashboard_concept.html", plot=bar)


# localhost:5000 /user/esempi marco
@app.route('/user/<name>')
def user(name):
    return render_template("ex4/user.html", user_name=name)


# invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("ex4/404.html"), 404


# name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()

    if form.validate_on_submit():
        # se l'utente scrive qualcosa allora metti il valore nella variabile user_naem
        name = form.name.data
        form.name.data = ''

    return render_template("ex4/name.html", name=name,
                           form=form)




if __name__ == '__main__':
    app.run()
