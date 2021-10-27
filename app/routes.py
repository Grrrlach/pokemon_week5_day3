from flask import render_template, request
import requests
from app import app
from .forms import PokemonForm

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