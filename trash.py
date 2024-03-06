models1 = [SwapiPeople(
            birth_year=it['birth_year'],
            eye_color=it['eye_color'],
            films=it['films'],
            gender=it['gender'],
            hair_color=it['hair_color'],
            height=it['height'],
            homeworld=it['homeworld'],
            mass=it['mass'],
            name=it['name'],
            skin_color=it['skin_color'],
            species=it['species'],
            starships=it['starships'],
            vehicles=it['vehicles']
        ) for it in list_of_json]
    # for it in list_of_json:
    #     print(it['name'])
    #     SwapiPeople(
    #         birth_year=it['birth_year'],
    #         eye_color=it['eye_color'],
    #         films=it['films'],
    #         gender=it['gender'],
    #         hair_color=it['hair_color'],
    #         height=it['height'],
    #         homeworld=it['homeworld'],
    #         mass=it['mass'],
    #         name=it['name'],
    #         skin_color=it['skin_color'],
    #         species=it['species'],
    #         starships=it['starships'],
    #         vehicles=it['vehicles']
    #     )
    #     models1.append(SwapiPeople)

async def insert_to_db(list_of_json):
    client = aiohttp.ClientSession()
    for link_fields in list_of_json:
        list_href_films = []
        list_href_species = []
        list_href_starships = []
        list_href_vehicles = []
        for href in link_fields['films']:
            http_response_films = await client.get(f'{href}')
            json_result_films = await http_response_films.json()
            film = json_result_films['title']
            list_href_films.append(film)
        for href in link_fields['species']:
            http_response_species = await client.get(f'{href}')
            json_result_species = await http_response_species.json()
            species = json_result_species['name']
            list_href_species.append(species)
        for href in link_fields['starships']:
            http_response_starships = await client.get(f'{href}')
            json_result_films = await http_response_starships.json()
            starships = json_result_films['name']
            list_href_starships.append(starships)
        for href in link_fields['vehicles']:
            http_response_vehicles = await client.get(f'{href}')
            json_result_vehicles = await http_response_vehicles.json()
            vehicles = json_result_vehicles['name']
            list_href_vehicles.append(vehicles)
        models = [SwapiPeople(
            birth_year=json_items['birth_year'],
            eye_color=json_items['eye_color'],
            films=', '.join(list_href_films),
            gender=json_items['gender'],
            hair_color=json_items['hair_color'],
            height=json_items['height'],
            homeworld=json_items['homeworld'],
            mass=json_items['mass'],
            name=json_items['name'],
            skin_color=json_items['skin_color'],
            species=', '.join(list_href_species),
            starships=', '.join(list_href_starships),
            vehicles=', '.join(list_href_vehicles)
        ) for json_items in list_of_json]
        async with Session() as session:
            session.add_all(models)
            await session.commit()

    async with aiohttp.ClientSession() as client:

        list_href_films = []
        list_href_species = []
        list_href_starships = []
        list_href_vehicles = []

        for link_fields in list_of_json:
            list_href_films.clear()
            list_href_species.clear()
            list_href_starships.clear()
            list_href_vehicles.clear()

            for link_films in link_fields["films"]:
                async with client.get(f'{link_films}') as http_response_films:
                    json_result_films = await http_response_films.json()
                    list_href_films.extend(json_result_films['title'])

            for link_species in link_fields["species"]:
                async with client.get(f'{link_species}') as http_response_species:
                    json_result_species = await http_response_species.json()
                    list_href_species.extend(json_result_species['name'])

            for link_starships in link_fields["starships"]:
                async with client.get(f'{link_starships}') as http_response_starships:
                    json_result_starships = await http_response_starships.json()
                    list_href_starships.extend(json_result_starships['name'])

            for link_vehicles in link_fields["vehicles"]:
                async with client.get(f'{link_vehicles}') as http_response_vehicles:
                    json_result_vehicles = await http_response_vehicles.json()
                    list_href_vehicles.extend(json_result_vehicles['name'])

            models = [
                SwapiPeople(
                    birth_year=json_items['birth_year'],
                    eye_color=json_items['eye_color'],
                    films=', '.join(list_href_films),
                    gender=json_items['gender'],
                    hair_color=json_items['hair_color'],
                    height=json_items['height'],
                    homeworld=json_items['homeworld'],
                    mass=json_items['mass'],
                    name=json_items['name'],
                    skin_color=json_items['skin_color'],
                    species=', '.join(list_href_species),
                    starships=', '.join(list_href_starships),
                    vehicles=', '.join(list_href_vehicles)
                ) for json_items in list_of_json
            ]

            async with Session() as session:
                session.add_all(models)
                await session.commit()
