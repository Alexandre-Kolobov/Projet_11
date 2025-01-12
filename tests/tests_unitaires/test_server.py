import server
from bs4 import BeautifulSoup
from datetime import datetime
from flask import url_for


def test_should_redirect_to_showSummary_if_email_exists(client):
    """correction bug/Entering-a-unknown-email-crashes-the-app"""
    email = "admin@irontemple.com"
    form_data = {"email": email}

    response = client.post('/showSummary', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    element_to_parse = soup.find("h2")
    string_to_test = f"Welcome, {email}"
    # print(element_to_parse)
    assert string_to_test in element_to_parse.text


def test_should_show_error_if_email_doesnt_exists(client):
    """correction bug/Entering-a-unknown-email-crashes-the-app"""
    email = "test@gmail.com"
    form_data = {"email": email}

    response = client.post('/showSummary', data=form_data)
    assert response.status_code == 302
    assert response.headers["location"] == url_for('index', _external=True)

    response = client.post('/showSummary', data=form_data, follow_redirects=True)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    element_to_parse = soup.find("ul", class_="message_flash")
    string_to_test = "Sorry, that email wasn't found."
    assert string_to_test in element_to_parse.text


def test_should_allow_booking_for_future_competition(mocker, client, competitions):
    response = client.get('/book/Competition dans le future/She Lifts')
    assert response.status_code == 200
    assert b"How many places?" in response.data


def test_should_not_allow_booking_for_past_competition(mocker, client, competitions):
    """correction bug/Booking-places-in-past-competitions"""

    # Test route /showSummary
    email = "admin@irontemple.com"
    form_data = {"email": email}

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
    response = client.get('/book/Spring Festival/She Lifts')
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    message = soup.find("ul", class_="message_flash")
    string_to_test = "You can't book places for past competition"
    assert string_to_test in message.text

    # Test route /purchasePlaces
    club = "Simply Lift"
    competition = "Competition dans le future"
    places = "1"

    form_data = {
        "club": club,
        "competition": competition,
        "places": places
        }

    mocker.patch.object(server, 'competitions', competitions)

    response = client.post('/purchasePlaces', data=form_data)
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


def test_should_return_code_200_when_purchasing_places(client):

    club = "Simply Lift"
    competition = "Spring Festival"
    places = "1"

    form_data = {
        "club": club,
        "competition": competition,
        "places": places}

    response = client.post('/purchasePlaces', data=form_data)

    assert response.status_code == 200


def test_should_not_update_points_of_competiton_when_reservation_was_cancelled(mocker, client, clubs, competitions):
    """correction bug/Competition_points_updated_even_if_reservation_was_canceled"""

    mocker.patch.object(server, 'competitions', competitions)
    mocker.patch.object(server, 'clubs', clubs)

    # Cas ou un club commande plus de place qu'ils ont des points
    club_name = "Simply Lift"

    for club in clubs:
        if club["name"] == club_name:
            club["points"] = 1

    competition_name = "Competition dans le future"
    for competition in competitions:
        if competition["name"] == competition_name:
            competition["numberOfPlaces"] = 25

    places = "2"

    form_data = {
        "club": club_name,
        "competition": competition_name,
        "places": places}

    selected_competition_data = [
        (competition["numberOfPlaces"], competition["date"])
        for competition in competitions
        if competition["name"] == form_data["competition"]
        ]

    selected_competition_places, selected_competition_date = selected_competition_data[0]

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    next_competitions = soup.find("ul", class_="next_competitions")

    string_to_test = (
        f'{competition_name} Date: {selected_competition_date} Number of Places: {selected_competition_places}'
        )
    assert string_to_test in next_competitions.text

    # Cas ou un club commande plus de 12 places
    club_name = "Simply Lift"

    for club in clubs:
        if club["name"] == club_name:
            club["points"] = 15

    competition_name = "Competition dans le future"
    for competition in competitions:
        if competition["name"] == competition_name:
            competition["numberOfPlaces"] = 20

    places = "16"

    form_data = {
        "club": club_name,
        "competition": competition_name,
        "places": places}

    selected_competition_data = [
        (competition["numberOfPlaces"], competition["date"])
        for competition in competitions
        if competition["name"] == form_data["competition"]
        ]

    (selected_competition_places,
     selected_competition_date) = selected_competition_data[0]

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    next_competitions = soup.find("ul", class_="next_competitions")

    string_to_test = (
        f'{competition_name} Date: {selected_competition_date} Number of Places: {selected_competition_places}'
        )
    assert string_to_test in next_competitions.text

    # Cas ou un un club commande plus de place qu'une competition a
    club_name = "Simply Lift"

    for club in clubs:
        if club["name"] == club_name:
            club["points"] = 15

    competition_name = "Competition dans le future"
    for competition in competitions:
        if competition["name"] == competition_name:
            competition["numberOfPlaces"] = 4

    places = "11"

    form_data = {
        "club": club_name,
        "competition": competition_name,
        "places": places}

    selected_competition_data = [
        (competition["numberOfPlaces"], competition["date"])
        for competition in competitions
        if competition["name"] == form_data["competition"]
        ]

    selected_competition_places, selected_competition_date = selected_competition_data[0]

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    next_competitions = soup.find("ul", class_="next_competitions")

    string_to_test = (
        f'{competition_name} Date: {selected_competition_date} Number of Places: {selected_competition_places}'
        )
    assert string_to_test in next_competitions.text


def test_should_update_points_of_competiton_when_reservation_validated(mocker, client, clubs, competitions):
    """correction bug/Competition_points_updated_even_if_reservation_was_canceled"""

    mocker.patch.object(server, 'competitions', competitions)
    mocker.patch.object(server, 'clubs', clubs)

    club_name = "Simply Lift"

    for club in clubs:
        if club["name"] == club_name:
            club["points"] = 15

    competition_name = "Competition dans le future"
    for competition in competitions:
        if competition["name"] == competition_name:
            competition["numberOfPlaces"] = 25

    places = "2"

    form_data = {
        "club": club_name,
        "competition": competition_name,
        "places": places}

    selected_competition_data = [
        (competition["numberOfPlaces"], competition["date"])
        for competition in competitions
        if competition["name"] == form_data["competition"]
        ]

    selected_competition_places, selected_competition_date = selected_competition_data[0]

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    next_competitions = soup.find("ul", class_="next_competitions")
    sum_places = int(selected_competition_places) - int(places)

    string_to_test = (
        f'{competition_name} Date: {selected_competition_date} Number of Places: {str(sum_places)}'
        )
    assert string_to_test in next_competitions.text


def test_should_update_points_of_club_when_purchasing_places(mocker, client, clubs, competitions):
    """correction bug/Point-updates-are-not-reflected"""

    mocker.patch.object(server, 'competitions', competitions)
    mocker.patch.object(server, 'clubs', clubs)

    club = "Simply Lift"
    competition = "Spring Festival"
    places = "1"

    form_data = {
        "club": club,
        "competition": competition,
        "places": places}

    selected_club_points = [club["points"] for club in clubs if club["name"] == form_data["club"]]
    points_update = int(selected_club_points[0])-int(places)

    string_to_test = f'Points available: {str(points_update)}'.encode('utf-8')

    response = client.post('/purchasePlaces', data=form_data)
    assert string_to_test in response.data


def test_should_book_0_to_12_places_par_competition_in_one_time(
        mocker, client, clubs, competitions, list_club_places_per_competition
        ):
    """correction bug/Clubs-should-not-be-able-to-book-more-than-12-places-per-competition"""
    mocker.patch.object(server, 'competitions', competitions)
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)

    club = "Simply Lift"
    competition = "Competition dans le future"
    places = "1"

    form_data = {
        "club": club,
        "competition": competition,
        "places": places}

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    message = soup.find("ul", class_="message_flash")
    string_to_test = "Great-booking complete!"
    assert string_to_test in message.text


def test_should_book_0_to_12_places_par_competition_in_many_times(
        mocker, client, clubs, competitions, list_club_places_per_competition
        ):
    """correction bug/Clubs-should-not-be-able-to-book-more-than-12-places-per-competition"""
    mocker.patch.object(server, 'competitions', competitions)
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)

    club = "Simply Lift"
    competition = "Competition dans le future"
    places = "1"

    form_data = {
        "club": club,
        "competition": competition,
        "places": places}

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


def test_should_not_book_more_than_12_places_par_competition_in_one_time(
        mocker, client, clubs, competitions, list_club_places_per_competition
        ):
    """correction bug/Clubs-should-not-be-able-to-book-more-than-12-places-per-competition"""
    mocker.patch.object(server, 'competitions', competitions)
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)

    club = "Simply Lift"
    competition = "Competition dans le future"
    places = "13"

    form_data = {
        "club": club,
        "competition": competition,
        "places": places}

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    message = soup.find("ul", class_="message_flash")
    string_to_test = "Error: you can't book more than 12 places per competition!"
    assert string_to_test in message.text


def test_should_not_book_more_than_12_places_par_competition_in_many_times(
        mocker, client, clubs, competitions, list_club_places_per_competition
        ):
    """correction bug/Clubs-should-not-be-able-to-book-more-than-12-places-per-competition"""
    mocker.patch.object(server, 'competitions', competitions)
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)

    club = "Simply Lift"
    competition = "Competition dans le future"
    places = "10"

    form_data = {
        "club": club,
        "competition": competition,
        "places": places}

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    message = soup.find("ul", class_="message_flash")
    # print(message)
    string_to_test = "Great-booking complete!"
    assert string_to_test in message.text

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    message = soup.find("ul", class_="message_flash")
    # print(message)
    string_to_test = "Error: you can't book more than 12 places per competition!"
    assert string_to_test in message.text


def test_should_not_update_club_points_if_reservation_error(
        mocker, client, clubs, competitions, list_club_places_per_competition
        ):
    """correction bug/Clubs-should-not-be-able-to-book-more-than-12-places-per-competition"""
    mocker.patch.object(server, 'competitions', competitions)
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)

    club_name = "Simply Lift"
    competition = "Competition dans le future"
    places = "13"

    form_data = {
        "club": club_name,
        "competition": competition,
        "places": places}

    expected_result = [club["points"] for club in clubs if club["name"] == club_name][0]

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    message = soup.find("body")
    string_to_test = f"Points available: {expected_result}"
    assert string_to_test in message.text


def test_club_should_use_points_to_book_places(mocker, client, clubs, competitions, list_club_places_per_competition):
    """correction bug/Clubs-should-not-be-able-to-use-more-than-their-points-allowed"""
    mocker.patch.object(server, 'competitions', competitions)
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)

    club_name = "Simply Lift"
    competition = "Competition dans le future"
    places = "6"

    for club in clubs:
        if club["name"] == club_name:
            club["points"] = 10
            club_points = club["points"]

    form_data = {
        "club": club_name,
        "competition": competition,
        "places": places}

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    message = soup.find("ul", class_="message_flash")
    # print(message)
    string_to_test = "Great-booking complete!"
    assert string_to_test in message.text

    expected_result = (int(club_points)-int(places))
    soup = BeautifulSoup(content, 'html.parser')
    message = soup.find("body")
    string_to_test = f"Points available: {str(expected_result)}"
    assert string_to_test in message.text


def test_club_should_not_use_more_points_they_have_to_book_places(
        mocker, client, clubs, competitions, list_club_places_per_competition
        ):
    """correction bug/Clubs-should-not-be-able-to-use-more-than-their-points-allowed"""
    mocker.patch.object(server, 'competitions', competitions)
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'list_club_places_per_competition', list_club_places_per_competition)

    club_name = "Simply Lift"
    competition = "Competition dans le future"

    for club in clubs:
        if club["name"] == club_name:
            club["points"] = 1

    places = "2"

    form_data = {
        "club": club_name,
        "competition": competition,
        "places": places}

    response = client.post('/purchasePlaces', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    message = soup.find("ul", class_="message_flash")
    # print(message)
    string_to_test = "Error: you can't book more places than points your club has"
    assert string_to_test in message.text


def test_should_show_table_with_clubs_points(mocker, client, competitions, clubs):
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'competitions', competitions)

    # Test fonctionnement sur route index
    response = client.get('/')
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find("table")
    headers = table.find_all('tr')[0].find_all('th')
    assert headers[0].text == "Clubs"
    assert headers[1].text == "Points"

    i = 1
    for club in clubs:
        table_body = table.find_all('tr')[i].find_all('td')
        assert table_body[0].text == club["name"]
        assert table_body[1].text == club["points"]
        i += 1

    # Test fonctionnement sur route showSummary
    email = "admin@irontemple.com"
    form_data = {"email": email}

    response = client.post('/showSummary', data=form_data)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find("table")
    headers = table.find_all('tr')[0].find_all('th')
    assert headers[0].text == "Clubs"
    assert headers[1].text == "Points"

    i = 1
    for club in clubs:
        table_body = table.find_all('tr')[i].find_all('td')
        assert table_body[0].text == club["name"]
        assert table_body[1].text == club["points"]
        i += 1
