from flask import Flask, render_template, request, jsonify
import json

from templates.plots import us_state_map, testing_plots
from templates.plots import hospital_resources_needed
#from templates.plots import globe_plot, bubble_map, us_county_map
from other_data import testing_centers, load_model

app = Flask(__name__)

results = testing_centers.run()

@app.route("/")
def globe_map():
    #globe_plot.run()
    return render_template("pages/globe-page.html")


# Global cases pages
@app.route("/globe_map")
def globe_map_copy():
    #globe_plot.run()
    return render_template("pages/globe-page.html")
    
@app.route("/coronavirus_bubble_map")
def coronavirus_bubble_map():
    #bubble_map.run()
    return render_template("pages/bubble-map-page.html")

@app.route("/global_data")
def global_data():
    return render_template("pages/global-data-page.html")


# US data pages
@app.route("/us_states_map")
def us_states_map():
    us_state_map.run()
    return render_template("pages/us-states-map-page.html")

@app.route("/us_counties_map")
def us_counties_map():
    #us_county_map.run()
    return render_template("pages/us-counties-map-page.html")

@app.route("/county_data")
def county_data():
    return render_template("pages/county-data-page.html")


@app.route("/global_testing")
def global_testing():
    testing_plots.run()
    return render_template("pages/testing-plots-page.html")

@app.route("/testing_data")
def testing_data():
    return render_template("pages/testing-data-page.html")


@app.route("/state_resources")
def state_resources():
    hospital_resources_needed.run()
    return render_template("pages/state-resources-page.html")

@app.route("/us_hospital_data")
def us_hospital_data():
    return render_template("pages/us-hospital-data-page.html")


# Top navbar pages
@app.route("/news")
def news():
    return render_template("pages/news-page.html")

@app.route("/about")
def about():
    return render_template("pages/about-me-page.html")

@app.route("/data")
def data():
    return render_template("pages/data-sources-page.html")

@app.route("/covid")
def covid():
    return render_template("pages/covid-info-page.html")


# Nearby testing page
@app.route("/nearby_testing")
def nearby_testing():
    return render_template("pages/testing-centers-page.html")

@app.route("/get_testing_centers")
def get_testing_centers():
    return json.dumps(results)


# Mortality calculator page
@app.route("/mortality_calc")
def mortality_calc():
    return render_template("pages/mortality-calc-page.html")

@app.route('/get_form_data', methods = ['POST'])
def get_form_data():
    jsdata = request.get_json()
    data = dict()
    for d in jsdata:
        data[d["name"]] = d["value"]
    prediction = load_model.predict(data)
    return jsonify(prediction)

    
if __name__ == "__main__":
    app.run(port=80, debug=True)