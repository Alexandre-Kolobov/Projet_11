import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
list_club_places_per_competition = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    club = [club for club in clubs if club['email'] == request.form['email']][0]
    
    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions,
        current_time=current_time
        )


@app.route('/book/<competition>/<club>')
def book(competition,club):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition and foundCompetition["date"] > current_time:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        if foundCompetition["date"] < current_time:
            flash("You can't book places for past competition")
        else:
            flash("Something went wrong-please try again")

        return render_template('welcome.html',
                               club=club,
                               competitions=competitions,
                               current_time=current_time)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    error_message_overbook_competition = "Error: you can't book more than 12 places per competition!"
    error_message_not_enought_points = "Error: you can't book more places than points your club has"
    validation_message = "Great-booking complete!"

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired

    #  correction bug/Point-updates-are-not-reflected and bug/Clubs-should-not-be-able-to-use-more-than-their-points-allowed
    if int(club['points'])-placesRequired < 0:
        flash(error_message_not_enought_points)
    else:
        club['points'] = int(club['points'])-placesRequired
    

    check_of_booked_places = [
        club_places_per_competition for club_places_per_competition in list_club_places_per_competition
        if club_places_per_competition["club_name"]==club["name"] and club_places_per_competition["competition_name"]==competition["name"]
        ]
    
    if check_of_booked_places:
        sum_of_places = int(check_of_booked_places[0]["booked_places"]) + placesRequired
        if sum_of_places > 12:
            flash(error_message_overbook_competition)
        else:
            check_of_booked_places[0]["booked_places"] = sum_of_places
            flash(validation_message)
    else:
        if placesRequired > 12:
            flash(error_message_overbook_competition)
        else:
            dict_club_places_per_competition = {
                "club_name":club["name"],
                "competition_name":competition["name"],
                "booked_places":placesRequired
            }
            list_club_places_per_competition.append(dict_club_places_per_competition)
            flash(validation_message)

    return render_template('welcome.html',
                           club=club,
                           competitions=competitions,
                           current_time=current_time)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))