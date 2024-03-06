import datetime
import asyncio
import aiohttp
import json
from more_itertools import chunked
from models import init_db, SwapiPeople, Session, engine
import requests
# from models1 import init_db1, SwapiPeople1, Session1, engine1


MAX_CHUNK = 20


async def get_person(client, person_id):
    http_response = await client.get(f'https://swapi.py4e.com/api/people/{person_id}/')
    json_result = await http_response.json()
    return json_result


async def insert_to_db(list_of_json):
    client = aiohttp.ClientSession()
    for link_fields in list_of_json:
        list_href_films = []
        list_href_species = []
        list_href_starships = []
        list_href_vehicles = []
        if 'films' in link_fields:
            for href in link_fields['films']:
                http_response_films = await client.get(f'{href}')
                json_result_films = await http_response_films.json()
                film = json_result_films['title']
                list_href_films.append(film)
        else:
            list_href_films.append('нет фильмов')
        if 'species' in link_fields:
            for href in link_fields['species']:
                http_response_species = await client.get(f'{href}')
                json_result_species = await http_response_species.json()
                species = json_result_species['name']
                list_href_species.append(species)
        else:
            list_href_species.append('нет типов')
        if 'starships' in link_fields:
            for href in link_fields['starships']:
                http_response_starships = await client.get(f'{href}')
                json_result_films = await http_response_starships.json()
                starships = json_result_films['name']
                list_href_starships.append(starships)
        else:
            list_href_starships.append('нет кораблей')
        if 'vehicles' in link_fields:
            for href in link_fields['vehicles']:
                http_response_vehicles = await client.get(f'{href}')
                json_result_vehicles = await http_response_vehicles.json()
                vehicles = json_result_vehicles['name']
                list_href_vehicles.append(vehicles)
        else:
            list_href_vehicles.append('нет транспорта')

        if 'birth_year' in link_fields:
            birth_year = link_fields['birth_year']
        else:
            birth_year = 'None'

        if 'eye_color' in link_fields:
            eye_color = link_fields['eye_color']
        else:
            eye_color = 'None'

        if 'gender' in link_fields:
            gender = link_fields['gender']
        else:
            gender = 'None'

        if 'hair_color' in link_fields:
            hair_color = link_fields['hair_color']
        else:
            hair_color = 'None'

        if 'height' in link_fields:
            height = link_fields['height']
        else:
            height = 'None'

        if 'homeworld' in link_fields:
            homeworld = link_fields['homeworld']
        else:
            homeworld = 'None'

        if 'mass' in link_fields:
            mass = link_fields['mass']
        else:
            mass = 'None'

        if 'skin_color' in link_fields:
            skin_color = link_fields['skin_color']
        else:
            skin_color = 'None'

        if 'skin_color' in link_fields:
            skin_color = link_fields['skin_color']
        else:
            skin_color = 'None'

        if 'name' in link_fields:
            name = link_fields['name']
        else:
            name = 'None'

        models = []

        people = SwapiPeople(
            birth_year=birth_year,
            eye_color=eye_color,
            films=', '.join(list_href_films),
            gender=gender,
            hair_color=hair_color,
            height=height,
            homeworld=homeworld,
            mass=mass,
            name=name,
            skin_color=skin_color,
            species=', '.join(list_href_species),
            starships=', '.join(list_href_starships),
            vehicles=', '.join(list_href_vehicles)
        )

        models.append(people)
        async with Session() as session:
            session.add_all(models)
            await session.commit()

    await client.close()
    await engine.dispose()


async def main():
    await init_db()
    client = aiohttp.ClientSession()
    count = 0
    url = 'https://swapi.dev/api/people/'

    while url:
        response = requests.get(url)
        json_data = response.json()
        count += json_data['count']
        url = json_data['next']

    for chunk in chunked(range(1, 3), 10):
        coros = [get_person(client, person_id) for person_id in chunk]
        result = await asyncio.gather(*coros)
        asyncio.create_task(insert_to_db(result))

    tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks_set)

    await client.close()
    await engine.dispose()

if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)