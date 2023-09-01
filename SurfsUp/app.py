# Import the dependencies.
import numpy as np

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask,jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"api/v1.0/precipitation<br/>"
        f"api/v1.0/stations<br/>"
        f"api/v1.0/tobs<br/>"
        f"api/v1.0/<start><br/>"
        f"api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the last 12 months of precipitation data
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).\
        order_by(Measurement.date).all()
    
    session.close()
    
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    precipitation = list(np.ravel(results))

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the last 12 months of temperature observation data for this station
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    # Query the min, max, and avg temps for all dates greater than and equal to the start date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Query the min, max, and avg temps for all dates greater than and equal to the start date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)