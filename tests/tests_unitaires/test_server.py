import server
from tests.tests_unitaires.conftest import client




def test_should_return_code_200_when_purchasing_places(client):
     
     club = "Simply Lift"
     competition = "Spring Festival"
     places = "1"

     form_data = {
          "club":club,
          "competition":competition,
          "places":places}

     response = client.post('/purchasePlaces', data=form_data)

     assert response.status_code == 200


def test_should_update_points_of_club_when_purchasing_places(mocker, client):
     """correction bug/Point-updates-are-not-reflected"""
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
          }
     ]

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

     mocker.patch.object(server, 'competitions', competitions)
     mocker.patch.object(server, 'clubs', clubs)


     club = "Simply Lift"
     competition = "Spring Festival"
     places = "1"

     form_data = {
          "club":club,
          "competition":competition,
          "places":places}
     
     selected_club_points = [club["points"] for club in clubs if club["name"]==form_data["club"]]
     points_update = int(selected_club_points[0])-int(places)

     string_to_test = f'Points available: {str(points_update)}'.encode('utf-8')

     response = client.post('/purchasePlaces', data=form_data)
     assert string_to_test in response.data