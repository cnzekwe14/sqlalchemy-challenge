from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect

app = Flask(__name__)

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#date greater than or equal to start date
start1 = session.query(Measurement.date).\
filter(Measurement.date >= "2011-09-11").all()
start1
startdict=[]
for number in start1:
    dates={}
    dates['Start'] = number
    startdict.append(dates)
startdict

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # create engine to hawaii.sqlite
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(autoload_with=engine)

    # View all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    Measurement = Base.classes.measurement

    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Find the most recent date in the data set.
    most_recent =session.query(func.max(Measurement.date)).first()

    ## Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. (prcp)

    # Calculate the date one year from the last date in data set.
    for x in most_recent:
        convert_mr = dt.datetime.strptime(x,'%Y-%m-%d')
    convert_mr #timestamp
    convert_my = convert_mr.strftime('%Y-%m-%d')#date
        

    previous12 = convert_mr - dt.timedelta(days=365) # timestamp
    previous13 = previous12.strftime('%Y-%m-%d') #date


    # Perform a query to retrieve the data and precipitation scores
    sel = [Measurement.id,Measurement.date,func.sum(Measurement.prcp)]

    # data_prcp = session.query(*sel).filter((Measurement.date <= convert_my) & (Measurement.date >=previous13)).\
    # group_by(Measurement.date).order_by(Measurement.date.desc()).all()
    data_prcp = session.query(Measurement.date,Measurement.prcp).\
    filter((Measurement.date <= convert_my) & (Measurement.date >=previous13)).all()


    # Create a dictionary from row data
    prcpdict =[]
    for date, prcp in data_prcp:
        prcp_dict = {date: prcp}
        prcpdict.append(prcp_dict)

    return jsonify(prcpdict)


@app.route("/api/v1.0/stations")
def station():  


     # create engine to hawaii.sqlite
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(autoload_with=engine)

    # View all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    station = Base.classes.station

    # Create our session (link) from Python to the DB
    session = Session(engine)

    all_stations = session.query(station.station).all()   
    
    stations1 = list(np.ravel(all_stations))
    
    return jsonify(stations1)

@app.route("/api/v1.0/tobs")
def tobs():

     # create engine to hawaii.sqlite
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(autoload_with=engine)

    # View all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    Measurement = Base.classes.measurement

    # Create our session (link) from Python to the DB
    session = Session(engine)

    recent = session.query(func.max(Measurement.date)).group_by(Measurement.station).\
    order_by(Measurement.id.desc()).first()

    for r in recent:
        convert_1 = dt.datetime.strptime(r,'%Y-%m-%d')
    convert_1 #timestamp
    convert_2 = convert_1.strftime('%Y-%m-%d')#date
        

    previous1 = convert_1 - dt.timedelta(days=365) # timestamp
    previous2 = previous1.strftime('%Y-%m-%d') #date
    high = session.query(Measurement.station).group_by(Measurement.station).\
    order_by(Measurement.id.desc()).first()

    high

    for r in high:
        i = r
    i
    data_station = session.query(Measurement.prcp).\
    filter((Measurement.station ==i)& (Measurement.date <= convert_2) & (Measurement.date >=previous2)).all()
    data_station

    temp = list(np.ravel(data_station))
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def start(start):
    "Find the min temp, avg temp and max temp for a specifed start range"
     # create engine to hawaii.sqlite
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(autoload_with=engine)

    # View all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    Measurement = Base.classes.measurement

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #min, avg and max temp for a start date
    
    for start in startdict:
        gel = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
        temperature_list = session.query(*gel).filter(Measurement.date == start).first()
        
    temp_1 = list(np.ravel(temperature_list))
    return jsonify(temp_1)




if __name__ == '__main__':
    app.run(debug=True)