###### Home Work ######

##Import

from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct


# In[ ]:

ß
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement=Base.classes.measurement
Station=Base.classes.station


# In[6]:


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
        f"Homework API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """A dictionary using 'date' as the key and 'prcp' as the value."""
    """Return the JSON representation of your dictionary."""
    # Query date and prcp
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        get_ipython().run_line_magic('pinfo2', 'prcp_dict')
        all_passengers.append(passenger_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    
    session = Session(engine)
    
    stations=session.query(distinct(Measurement.station)).all()
    
    session.close()

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of stations from the dataset"""
    
    session = Session(engine)
    
    station_cnt=session.query(Measurement.station,func.count(Measurement.station)).        group_by(Measurement.station).        order_by(func.count(Measurement.station).desc()).all()
    
    temp_l12_highest_act = session.query(Measurement.date,Measurement.tobs).        filter(Measurement.station == station_cnt[0][0]).        filter(Measurement.date >= last12m).all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for date, tobs in temp_l12_highest_act:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["prcp"] = tobs
        all_tobs.append(tobs_dict)
        
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_range(start):
    """Return a JSON list of the minimum temperature, the average temperature, 
    and the max temperature for a given start."""
    
    temp = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]

    tobs_start = session.query(*temp).    filter(Measurement.date >= start).all()

    if len(tobs_start) == 1:
            return jsonify(tobs_start)

    return jsonify({"error": f"Date {start} not found."})


@app.route("/api/v1.0/<start>/<end>")
def start_range(start,end):
    """Return a JSON list of the minimum temperature, the average temperature, 
    and the max temperature for a given start-end range."""
    
    temp = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]

    tobs_start = session.query(*temp).    filter(Measurement.date >= start).    filter(Measurement.date <= end).all()

    if len(tobs_start) == 1:
            return jsonify(tobs_start)

    return jsonify({"error": f"Date {start} or {end} not found."})



if __name__ == "__main__":
    app.run(debug=True)

