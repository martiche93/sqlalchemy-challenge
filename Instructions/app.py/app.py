import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, MetaData
from flask import Flask, jsonify

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

base = automap_base()
base.prepare(engine, reflect=True)

measurement = base.classes.measurement
station = base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def homepage():
    return(f"Hello world! Welcome to my API. Listed below are the available routes: <br/>"
           f"/api/v1.0/prcp<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
           f"/api/v1.0/[start format:yyyy-mm-dd]/[end_date:yyyy-mm-dd]<br/>")


@app.route("/api/v1.0/prcp")
def prcp():
    session = Session(engine)

    year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    recent_date = session.query(measurement.date).order_by(
        measurement.date.desc()).first()
    prcp = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > year_before).order_by(measurement.date).all()

    prcp_list = []
    for date, prcp in prcp_list:
        dict = {}
        dict["date"] = date
        dict["prcp"] = prcp
        prcp_list.append(dict)
    return jsonify(prcp_list)


session.close()


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations_active = (session.query(measurement.station, func.count(measurement.station)).
                       group_by(measurement.station).order_by(func.count(measurement.station).desc()).all())

    return jsonify(stations_active)


session.close()


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    active_stations = (session.query(measurement.station, func.count(measurement.station)).
                       group_by(measurement.station).order_by(func.count(measurement.station).desc()).all())
    most_active = active_stations[0][0]
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= "2016-08-24").\
        filter(measurement.date <= "2017-08-24").\
        filter(measurement.station == most_active).all()

    return jsonify(results)

    session.close()


@app.route("/api/v1.0/<start_date>")
def start(start_date):

    session = Session(engine)

    results = session.query(func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).\
        filter(measurement.date >= start_date).all()


session.close()


@app.route("/api/v1.0/<start_date>")
def start(start_date):

    session = Session(engine)

    results = session.query(func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).\
        filter(measurement.date >= start_date).all()

    session.close()

    list = []
    for avg, max, min in results:
        dict = {}
        dict["avg_temp"] = avg
        dict["max_temp"] = max
        dict["min_temp"] = min
        list.append(dict)

    return jsonify(list)


@app.route("/api/v1.0/<start>/<end>")
def start_stop(start, end):

    session = Session(engine)

    results = session.query(func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()

    list = []
    for avg, max, min in results:
        dict = {}
        dict["avg_temp"] = avg
        dict["max_temp"] = max
        dict["min_temp"] = min
        list.append(dict)

    return jsonify(list)


if __name__ == '__main__':
    app.run(debug=True)
