import inquirer
import pyttsx3
import requests
from image import DrawImage
from pyfiglet import Figlet
from rich import print

engine = pyttsx3.init()

def num_validator(_, y):
    try:
        int(y)
        return True
    except:
        raise inquirer.errors.ValidationError(
            '', reason='That isn\'t a very good number')


def main():
    image = DrawImage.from_file("pokemon_logo.png", size=(70, 35))
    image.draw_image()
    title = Figlet(font="slant")
    print("[blue]" + title.renderText('Poke Dexter'))
    engine.say("Poke Dexter....- the C.L.I Pokedex")
    engine.runAndWait()
    questions = [
        inquirer.Text(
            'limit', message="How many Pokemon do you want to fetch?", validate=num_validator)
    ]
    answers = inquirer.prompt(questions)
    poke_list = poke_lister(answers['limit'])
    poke_choices = []
    for item in poke_list:
        poke_choices.append(item['name'].capitalize())
    pokemon_selected = inquirer.list_input("Pokemons", choices=poke_choices)
    poke_display(poke_fetcher(pokemon_selected))


def poke_lister(limit: int):
    poke_list = requests.get(
        f"https://pokeapi.co/api/v2/pokemon?limit={limit}")
    return poke_list.json()['results']


def poke_fetcher(pokemon: str):
    pokemon_data = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}")
    if pokemon_data.status_code != 200:
        raise ValueError("Error fetching data.")
    return pokemon_data.json()


def poke_display(pokemon: dict):
    poke_image = DrawImage.from_url(
        pokemon['sprites']['front_default'], size=(70, 35))
    poke_image.draw_image()
    header_disp = Figlet(font="slant")
    print("[green]" + header_disp.renderText(pokemon['species']['name'].capitalize()))
    print(f"[blue]{poke_desc_fetcher(poke_fetcher(pokemon['species']['name']))}")
    engine.say(pokemon['species']['name'] + ".. " + poke_desc_fetcher(poke_fetcher(pokemon['species']['name'])))
    engine.runAndWait()
    print(f"[blue]Weight: {pokemon['weight']}")
    print(f"[blue]Height: {pokemon['height']}")
    print(f"[yellow]Types: ")
    for x in pokemon['types']:
        print(f"[yellow]- {x['type']['name'].capitalize()}")
    print(f"[orange1]Base stats: ")
    for x in pokemon['stats']:
        print(
            f"[orange1]- {x['stat']['name'].capitalize()} = {x['base_stat']}")


def poke_desc_fetcher(pokemon: dict):
    pokemon_desc = requests.get(
        f"https://pokeapi.co/api/v2/pokemon-species/{pokemon['id']}")
    if pokemon_desc.status_code != 200:
        return "Couldn't get the description, chaps! Maybe next time?"
    pokemon_desc = pokemon_desc.json()['flavor_text_entries']
    english_desc = ''
    for x in pokemon_desc:
        if x['language']['name'] == 'en':
            english_desc = x['flavor_text']
    return(english_desc)


if __name__ == "__main__":
    main()
