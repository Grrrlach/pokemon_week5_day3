from flask import render_template, request, redirect, url_for
import requests
from app import app
from .forms import PokemonForm, LoginForm, RegisterForm, PasswordField
from wtforms.validators import EqualTo, DataRequired, ValidationError
from .models import User
from flask_login import login_user, current_user, logout_user, login_required

#Routes originally from app.py

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')


@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
# @app.route('/pokemon', methods=['GET', 'POST'])
# def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        poke_id = request.form.get('poke_id')
        url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
        response = requests.get (url)
        if response.ok:
            #the request worked
            if not response.json():
                return "We had an error loading your data likely the Pokemon is not in the database"
            data = response.json()
                
            poke_dict={
                'poke_name': data ['forms'][0] ['name'],
                'hp_base': data ['stats'][0] ['base_stat'],
                'attack_base': data ['stats'][1] ['base_stat'],
                'defense_base': data ['stats'][2] ['base_stat'],
                'front_shiny_sprite': data ['sprites']['front_shiny']
            }
            print(poke_dict)
            return render_template('pokemon.html.j2', pokemon_stats = poke_dict, form=form)
        else:
            return "Ain't gonna catch that 'un! That's no pokemon. Go back to search again!"
            #the request failed
                #format is: name inside of my html = name in python
    return render_template('pokemon.html.j2', form=form)

@app.route('/login', methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit:
        #do login stuff
        email = request.form.get('email').lower()
        password = request.form.get('password')

        u = User.query.filter_by(email=email).first()

        if u and u.check_hashed_password(password):
            login_user(u)
            #will want to give the user feedback saying successful login
            return redirect (url_for("index"))
        # else: #not necessary, could unindent the else statement, because of the return in the if statement
        # if email in app.config.get('REGISTERED_USERS') and \
        #     password == app.config.get('REGISTERED_USERS').get(email).get(password): THESE 3 LINES DEPRECATED BY U.CHECK_HASHED_PASSWORD
            # return f"Welcome, Pokemon trainer! {app.config.get('REGISTERED_USERS').get(email).get(name)}"
        error_string = "I think you may have come to the wrong place. We couldn't log you in with that info."
        return render_template('register.html.j2', error = error_string, form=form)
    return render_template('login.html.j2', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data,
                # "confirm_password":form.confirm_password.data,
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data) 
            #we just built a user with form data (1st line)
            #using the method in the user class to retrieve the data (2nd line)
            #save that user to the database, below
            new_user_object.save()
        except:
            error_string = "Beedrills got in our machine! Something went wront with your registration. Come back when we've caught them and patched up!"
            return render_template ('register.html.j2', form = form, error=error_string)
        return redirect(url_for('register'))
    return render_template('register.html.j2', form = form)
    
