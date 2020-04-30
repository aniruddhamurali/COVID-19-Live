from flask import Flask, render_template

from templates.plots import us_state_map, testing_plots
#from templates.plots import globe_plot, bubble_map, us_county_map

app = Flask(__name__)

@app.route("/")
def globe_map():
    #globe_plot.run()
    return render_template("pages/globe-page.html")


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

    
if __name__ == "__main__":
    app.run(debug=True)