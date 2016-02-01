import datetime
from peewee import *

from CrewScoreboard import app

class BaseModel(Model):
    class Meta:
        database = app.db

class Team(BaseModel):
    name = CharField()
    points = IntegerField()
    team_color = CharField()

class Student(BaseModel):
    name = TextField()
    team = ForeignKeyField(Team, related_name='students')

def create_tables():
    app.db.connect()
    app.db.create_tables([Team, Student])