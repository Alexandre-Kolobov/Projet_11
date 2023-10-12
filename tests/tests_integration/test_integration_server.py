from server import competitions, clubs
from bs4 import BeautifulSoup
from datetime import datetime

def test_login_summary_book_purchase_logout(client):
    email = clubs[0]["email"]
    form_data_login = {"email":email}

    response = client.post('/showSummary', data=form_data_login)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    element_to_parse = soup.find("h2")
    string_to_test = f"Welcome, {email}"

    assert response.status_code == 200
    assert string_to_test in element_to_parse.text

    soup = BeautifulSoup(content, 'html.parser')
    next_competitions = soup.find("ul", class_="next_competitions")
    for competition in competitions:
        if competition["date"] > datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
            competition_name = competition["name"]
            break

    club_name = [club["name"] for club in clubs if club["email"]==email][0]

    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200
    assert b"How many places?" in response.data
    for_data_book = {
        "club":club_name,
        "competition":competition_name,
        "places":1
        }

    response = client.post('/purchasePlaces', data=for_data_book)
    content = response.data
    soup = BeautifulSoup(content, 'html.parser')
    message = soup.find("ul", class_="message_flash")
    string_to_test = "Great-booking complete!"
    assert string_to_test in message.text

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

    string_to_test = "Welcome to the GUDLFT Registration Portal!"
    assert string_to_test.encode() in response.data



