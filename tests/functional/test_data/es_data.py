index_list = ['movies', 'persons', 'genres']

test_genres = [
    {
        'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
        'name': 'Action'
    },
    {
        'id': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd',
        'name': 'Fantasy'
    },
]

FANTASY_GENRE_FILM = {
    "id": "025c58cd-1b7e-43be-9ffb-8571a613579b",
    "imdb_rating": 8.3,
    "title": "Star Wars: Episode VI - Return of the Jedi",
    "description": "Luke Skywalker battles horrible Jabba the Hut and cruel Darth Vader to save his comrades in the Rebel Alliance and triumph over the Galactic Empire. Han Solo and Princess Leia reaffirm their love and team with Chewbacca, Lando Calrissian, the Ewoks and the androids C-3PO and R2-D2 to aid in the disruption of the Dark Side and the defeat of the evil emperor.",
    "genre": [
        {
            "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
            "name": "Fantasy"
        }
    ],
    "directors": [
        {
            "id": "3214cf58-8dbf-40ab-9185-77213933507e",
            "full_name": "Richard Marquand"
        }
    ],
    "actors": [
        {
            "id": "26e83050-29ef-4163-a99d-b546cac208f8",
            "full_name": "Mark Hamill"
        },
        {
            "id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1",
            "full_name": "Harrison Ford"
        },
        {
            "id": "b5d2b63a-ed1f-4e46-8320-cf52a32be358",
            "full_name": "Carrie Fisher"
        },
        {
            "id": "efdd1787-8871-4aa9-b1d7-f68e55b913ed",
            "full_name": "Billy Dee Williams"
        }
    ],
    "writers": [
        {
            "id": "3217bc91-bcfc-44eb-a609-82d228115c50",
            "full_name": "Lawrence Kasdan"
        },
        {
            "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
            "full_name": "George Lucas"
        }
    ]
}

ADVENTURE_GENRE_FILM = {
    "id": "cd54d6fb-0aa4-4262-845f-6d32665613a8",
    "imdb_rating": 6.8,
    "title": "Star Wars: Return of the Jedi - Death Star Battle",
    "description": None,
    "genre": [
        {
            "id": "120a21cf-9097-479e-904a-13dd7198c1dd",
            "name": "Adventure"
        },
    ],
    "directors": [],
    "actors": [],
    "writers": []
}

MULTIPLE_GENRE_FILM = {
    "id": "b503ced6-fff1-493a-ad41-73449b55ffee",
    "imdb_rating": 8.2,
    "title": "Star Wars: The Clone Wars",
    "description": "Jedi Knights lead the Grand Army of the Republic against the droid army of the Separatists.",
    "genre": [
        {
            "id": "120a21cf-9097-479e-904a-13dd7198c1dd",
            "name": "Adventure"
        },
        {
            "id": "1cacff68-643e-4ddd-8f57-84b62538081a",
            "name": "Drama"
        },
        {
            "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
            "name": "Action"
        },
        {
            "id": "6a0a479b-cfec-41ac-b520-41b2b007b611",
            "name": "Animation"
        },
        {
            "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
            "name": "Sci-Fi"
        },
        {
            "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
            "name": "Fantasy"
        }
    ],
    "directors": [],
    "actors": [
        {
            "id": "5237aac5-f652-4aa5-9061-55bb007cd7be",
            "full_name": "Tom Kane"
        },
        {
            "id": "8746ff78-577b-4bef-a7f7-1db05a102def",
            "full_name": "James Arnold Taylor"
        },
        {
            "id": "976fdf00-4f46-429b-af5b-2ddf2ff1b7c5",
            "full_name": "Matt Lanter"
        },
        {
            "id": "a3468637-c3c3-442c-892e-1625385c49c6",
            "full_name": "Dee Bradley Baker"
        }
    ],
    "writers": [
        {
            "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
            "full_name": "George Lucas"
        }
    ]
}

test_films = [
    FANTASY_GENRE_FILM,
    ADVENTURE_GENRE_FILM,
    MULTIPLE_GENRE_FILM
]

FILM_FOR_TEST_CACHE = {
    "id": "020adfa7-7251-4fb9-b6db-07b60664cb67",
    "imdb_rating": 6.9,
    "genre":
        [
            {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"},
            {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
            {"id": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"}
        ],
    "title": "Trek",
    "description": "Kirk and Spock team up against the Gorn.",
    "directors": [],
    "actors": [
        {"id": "8a34f121-7ce6-4021-b467-abec993fc6cd", "full_name": "Zachary Quinto"},
        {"id": "f89a9bad-5bd3-446d-bbdf-e1fd0d217e5d", "full_name": "John Cho"},
        {"id": "9f38323f-5912-40d2-a90c-b56899746f2a", "full_name": "Chris Pine"},
        {"id": "2cf03687-ebc3-47dc-a99f-602f6cc55f7a", "full_name": "Simon Pegg"}
    ],
    "writers": [
        {"id": "82b7dffe-6254-4598-b6ef-5be747193946", "full_name": "Alex Kurtzman"},
        {"id": "69e600f2-2cc2-4473-be29-3e61ebfd883c", "full_name": "Marianne Krawczyk"},
        {"id": "9b58c99a-e5a3-4f24-8f67-a038665758d6", "full_name": "Roberto Orci"}
    ],
}

test_persons = [
    {
        'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a',
        'full_name': 'George Lucas',
        'films': [
            {
                'id': '025c58cd-1b7e-43be-9ffb-8571a613579b',
                'roles': [
                    'writer'
                ]
            },
            {
                'id': 'b503ced6-fff1-493a-ad41-73449b55ffee',
                'roles': [
                    'writer'
                ]
            }
        ]
    },
    {
        'id': '26e83050-29ef-4163-a99d-b546cac208f8',
        'full_name': 'Mark Hamill',
        'films': [
            {
                'id': '025c58cd-1b7e-43be-9ffb-8571a613579b',
                'roles': [
                    'actor'
                ]
            }
        ]
    }
]
