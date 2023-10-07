import pytest

from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def clubs():
    clubs = [
        {
           'name': 'Simply Lift',
           'email': 'john@simplylift.co',
           'points': '10'
        },
        {
            'name': 'Iron Temple',
            'email': 'admin@irontemple.com',
            'points': '10'
        },
        {
            'name': 'She Lifts',
            'email': 'kate@shelifts.co.uk',
            'points': '10'
        }
    ]
    return clubs

@pytest.fixture
def competitions():
    competitions = [
        {
            'name': 'Spring Festival',
            'date': '2020-03-27 10:00:00',
            'numberOfPlaces': '25'
        },
        {
            'name': 'Fall Classic',
            'date': '2020-10-22 13:30:00',
            'numberOfPlaces': '13'
        },
        {
            "name": "Competition dans le future",
            "date": "2029-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Competition dans le future2",
            "date": "2030-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]
    return competitions

@pytest.fixture
def list_club_places_per_competition():
    list_club_places_per_competition = []

    return list_club_places_per_competition