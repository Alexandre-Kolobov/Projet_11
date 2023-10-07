import server
from bs4 import BeautifulSoup
from datetime import datetime

"""
Liste de test à réaliser:
Error trouvés:
     Pour '/book/<competition>/<club>' if else à tester
"""


def test_should_return_code_200_when_connected(client):
     
     email = "admin@irontemple.com"
     form_data = {"email":email}

     response = client.post('/showSummary', data=form_data)

     assert response.status_code == 200


def test_should_not_allow_booking_for_past_competition(mocker, client, competitions):
     """correction bug/Booking-places-in-past-competitions"""

     # Test route /showSummary
     email = "admin@irontemple.com"
     form_data = {"email":email}

     mocker.patch.object(server, 'competitions', competitions)

     response = client.post('/showSummary', data=form_data)
     content = response.data
     soup = BeautifulSoup(content, 'html.parser')
     next_competitions = soup.find("ul", class_="next_competitions")
     past_competitions = soup.find("ul", class_="past_competitions")
     for competition in competitions:
          if competition["date"] > datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
               # print(f"{competition['name']} is in next competitions")
               assert competition["name"] in next_competitions.text
          else:
               # print(f"{competition['name']} is in past competitions")
               assert competition["name"] in past_competitions.text


     # Test route /book/<competition>/<club>
     response = client.post('/book/Spring Festival/club_not_exists')
     content = response.data
     soup = BeautifulSoup(content, 'html.parser')
     next_competitions = soup.find("ul", class_="next_competitions")
     past_competitions = soup.find("ul", class_="past_competitions")
     print(soup)
     for competition in competitions:
          if competition["date"] > datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
               # print(f"{competition['name']} is in next competitions")
               assert competition["name"] in next_competitions.text
          else:
               # print(f"{competition['name']} is in past competitions")
               assert competition["name"] in past_competitions.text

     # Test route /purchasePlaces
     club = "Simply Lift"
     competition = "Competition dans le future"
     places = "1"

     form_data = {
          "club":club,
          "competition":competition,
          "places":places
          }

     mocker.patch.object(server, 'competitions', competitions)

     response = client.post('/purchasePlaces', data=form_data)
     content = response.data
     soup = BeautifulSoup(content, 'html.parser')
     next_competitions = soup.find("ul", class_="next_competitions")
     past_competitions = soup.find("ul", class_="past_competitions")
     for competition in competitions:
          if competition["date"] > datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
               print(f"{competition['name']} is in next competitions")
               assert competition["name"] in next_competitions.text
          else:
               print(f"{competition['name']} is in past competitions")
               assert competition["name"] in past_competitions.text


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


def test_should_update_points_of_club_when_purchasing_places(mocker, client, clubs, competitions):
     """correction bug/Point-updates-are-not-reflected"""

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


def test_should_book_0_to_12_places_par_competition_in_one_time(mocker, client, clubs, competitions, list_club_places_per_competition):
     """correction bug/Clubs-should-not-be-able-to-book-more-than-12-places-per-competition"""
     mocker.patch.object(server, 'competitions', competitions)
     mocker.patch.object(server, 'clubs', clubs)
     mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)


     club = "Simply Lift"
     competition = "Competition dans le future"
     places = "1"

     form_data = {
          "club":club,
          "competition":competition,
          "places":places}
     
     response = client.post('/purchasePlaces', data=form_data)
     content = response.data
     soup = BeautifulSoup(content, 'html.parser')
     message = soup.find("ul", class_="message_flash")
     string_to_test = "Great-booking complete!"
     assert string_to_test in message.text

def test_should_book_0_to_12_places_par_competition_in_many_times(mocker, client, clubs, competitions, list_club_places_per_competition):
     """correction bug/Clubs-should-not-be-able-to-book-more-than-12-places-per-competition"""
     mocker.patch.object(server, 'competitions', competitions)
     mocker.patch.object(server, 'clubs', clubs)
     mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)


     club = "Simply Lift"
     competition = "Competition dans le future"
     places = "1"

     form_data = {
          "club":club,
          "competition":competition,
          "places":places}
     
     response = client.post('/purchasePlaces', data=form_data)
     content = response.data
     soup = BeautifulSoup(content, 'html.parser')
     message = soup.find("ul", class_="message_flash")
     string_to_test = "Great-booking complete!"
     assert string_to_test in message.text

     response = client.post('/purchasePlaces', data=form_data)
     content = response.data
     soup = BeautifulSoup(content, 'html.parser')
     message = soup.find("ul", class_="message_flash")
     string_to_test = "Great-booking complete!"
     assert string_to_test in message.text


def test_should_not_book_more_than_12_places_par_competition_in_one_time(mocker, client, clubs, competitions, list_club_places_per_competition):
     """correction bug/Clubs-should-not-be-able-to-book-more-than-12-places-per-competition"""
     mocker.patch.object(server, 'competitions', competitions)
     mocker.patch.object(server, 'clubs', clubs)
     mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)


     club = "Simply Lift"
     competition = "Competition dans le future"
     places = "13"

     form_data = {
          "club":club,
          "competition":competition,
          "places":places}
     
     response = client.post('/purchasePlaces', data=form_data)
     content = response.data
     soup = BeautifulSoup(content, 'html.parser')
     message = soup.find("ul", class_="message_flash")
     string_to_test = "Error: you can't book more than 12 places per competition!"
     assert string_to_test in message.text


def test_should_not_book_more_than_12_places_par_competition_in_many_times(mocker, client, clubs, competitions, list_club_places_per_competition):
     """correction bug/Clubs-should-not-be-able-to-book-more-than-12-places-per-competition"""
     mocker.patch.object(server, 'competitions', competitions)
     mocker.patch.object(server, 'clubs', clubs)
     mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)


     club = "Simply Lift"
     competition = "Competition dans le future"
     places = "10"

     form_data = {
          "club":club,
          "competition":competition,
          "places":places}
     
     response = client.post('/purchasePlaces', data=form_data)
     content = response.data
     soup = BeautifulSoup(content, 'html.parser')
     message = soup.find("ul", class_="message_flash")
     print(message)
     string_to_test = "Great-booking complete!"
     assert string_to_test in message.text

     response = client.post('/purchasePlaces', data=form_data)
     content = response.data
     soup = BeautifulSoup(content, 'html.parser')
     message = soup.find("ul", class_="message_flash")
     print(message)
     string_to_test = "Error: you can't book more than 12 places per competition!"
     assert string_to_test in message.text

     