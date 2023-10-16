from locust import HttpUser, task, between
import json
import random


class PerfTest(HttpUser):
    wait_time = between(0, 2)

    with open('../../clubs.json') as c:
        clubs = json.load(c)['clubs']

    with open('../../competitions.json') as comps:
        competitions = json.load(comps)['competitions']

    def on_start(self):
        self.random_club = self.clubs.pop(0)
        self.random_competition = random.choice(self.competitions)

    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", data={"email": self.random_club["email"]})

    @task
    def book(self):
        self.client.get(f"/book/{self.random_competition['name']}/{self.random_club['name']}")

    @task
    def purchase(self):
        form_data = {
            "club": self.random_club['name'],
            "competition": self.random_competition['name'],
            "places": 1
            }
        self.client.post("/purchasePlaces", data=form_data)

    @task
    def logout(self):
        self.client.get("/logout")
