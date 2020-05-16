import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session=Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end")

@app.route("/api/v1.0/precipitation")
def precipitation():
        """return precipitation data from last year"""
        last_year=dt.date(2017,8,23)-dt.timedelta(days=365)
        results=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=last_year).all()
        prcp={date:precipitation for date,precipitation in results}
        return jsonify(prcp) 

@app.route("/api/v1.0/stations")
def stations():
    results=session.query(Station).all()
    all_stations=[]
    for station in results:
        station_dict={}
        station_dict['station']=station.station
        all_stations.append (station_dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tempature():
    last_year=dt.date(2017,8,23)-dt.timedelta(days=365)
    results=session.query(Measurement.tobs).filter(Measurement.date>=last_year).filter(Measurement.station=='USC00519281').all()
    results=list(np.ravel(results))
    return jsonify(results)

@app.route("/api/v1.0/temp/<start>/<end>")
def dynamic_start_end():
    results=sesssion.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    results=list(np.ravel(results))
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)