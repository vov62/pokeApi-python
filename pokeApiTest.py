
import requests
import json
import random



base_url =  'https://pokeapi.co/api/v2/pokemon'
limit = 200
url=f"{base_url}?limit={limit}"
pokemon_url =  'https://pokeapi.co/api/v2/pokemon'


def fetch_pokemons_data():

    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
    else:
        print(f'Error: fetching data failed! {res.status_code}')

    pokemon_list = data['results']
    return pokemon_list



def fetch_single_pokemon_details(random_pokemon_name):

    res = requests.get(f'{base_url}/{random_pokemon_name}')
    if res.status_code == 200:
        data = res.json()
    else:
        print(f'Error: fetching data failed! {res.status_code}')
    pokemon_details_data = data

    # Pokemon types values 
    pokemon_type_names  = []
    for type in pokemon_details_data['types']:
        pokemon_type_names.append(type['type']['name'])

    
    # extract pokemon another values 
    id  = pokemon_details_data['id']
    name = pokemon_details_data['name']
    height = pokemon_details_data['height']
    weight = pokemon_details_data['weight']


    # object to be appended
    pokemon_details = {
        "id": id,
        "name": name,
        "height": height,
        "weight": weight,
        "types": pokemon_type_names
    }

    # send data to json file

    try:
        
        with open('db.json', 'r+') as f:

            file_data = json.load(f)
            file_data["pokemons_db"].append(pokemon_details)
            f.seek(0)
            f.truncate()
            json.dump(file_data, f, indent= 4 )
            print('success, Pokemon details saved to database!')
            print('---------Pokemon details:-------------------')
            print(f"Pokémon: {name}\nID: {id}\nHeight: {height}\nWeight: {weight} \nTypes: {pokemon_type_names}")

    
    except Exception:
         print('Error: error sending json file')
    
    return pokemon_details_data




def select_random_pokemon():

    pokemon_list = fetch_pokemons_data()

    # randomly select a Pokémon from the list
    random_pokemon = random.choice(pokemon_list)
    random_pokemon_name = random_pokemon['name']
    print('Random Pokemon was chosen.')

    # print(random_pokemon_name)
    return random_pokemon_name



def check_if_pokemon_in_json():

    # check if Pokémon name is already in our JSON file

    random_pokemon_name = select_random_pokemon()
    is_found = False 
    
    try:
        with open("db.json","r") as f:
            json_data = json.load(f)
            
            for field_name in json_data["pokemons_db"]:
                if field_name['name'] == random_pokemon_name:
                    id = field_name['id']
                    name = field_name['name']
                    weight = field_name['weight']
                    height = field_name['height']
                    types = field_name['types']
                    print('found match!')
                    print('-----------Pokemon details from database------')
                    print(f"Pokémon: {name}\nID: {id}\nHeight: {height}\nWeight: {weight} \nTypes: {types}")
                    is_found = True
                    
            if not is_found:
                print('Error: pokemon name is not found in database')
                fetch_single_pokemon_details(random_pokemon_name)
                
    except:
        print('Error: error fetching json file')




def main():

    while True:
        userValue = input("Would you like to draw a Pokemon? yes/ no?: ").lower()
        if userValue == 'yes':
            check_if_pokemon_in_json()
            break
        elif userValue == 'no':
            print('Goodbye, exiting...')
        
        else:
            print('Enter only yes or no')

main()