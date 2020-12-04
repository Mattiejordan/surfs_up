#9.5.1
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#9.4.3

#pip install flask
from flask import Flask

app = Flask(__name__)

#@app.route('/')
def hello_world():
    return 'Hello world'

#export FLASK_APP=app.py
# set FLASK_APP=app.py
# flask run 

#9.5.1 Set up the database
#not sure if it goes in here or a jupyter notebook???

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#set up flask
app = Flask(__name__)
import app

print("example __name__ = %s", __name__)

if __name__ == "__main__":
    print("example is being run directly.")
else:
    print("example is being imported")

# set up routes AFTER the app=Flask(__name__)
#9.5.2
#@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
# in command line flask run

#9.5.3
#@app.route("/api/v1.0/precipitation")

# def precipitation():
#    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#    precipitation = session.query(Measurement.date, Measurement.prcp).\
#       filter(Measurement.date >= prev_year).all()
#    return
# JASONIFY IT

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#9.5.4
#@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#9.5.5
#@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#9.5.6
#@app.route("/api/v1.0/temp/<start>")
#@app.route("/api/v1.0/temp/<start>/<end>")

# def stats(start=None, end=None):
#     sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

#     if not end:
#         results = session.query(*sel).\
#             filter(Measurement.date >= start).\
#             filter(Measurement.date <= end).all()
#         temps = list(np.ravel(results))
#         return jsonify(temps=temps)

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#flask run