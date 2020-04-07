from flask import Flask, render_template      

app = Flask(__name__)

@app.route("/")
def globe_map():
    return render_template("pages/globe-page.html")

@app.route("/globe_map")
def globe_map_copy():
    return render_template("pages/globe-page.html")

    
@app.route("/coronavirus_bubble_map")
def coronavirus_bubble_map():
    return render_template("pages/bubble-map-page.html")

@app.route("/us_states_map")
def us_states_map():
    return render_template("pages/us-states-map-page.html")

@app.route("/us_counties_map")
def us_counties_map():
    return render_template("pages/us-counties-map-page.html")

    
if __name__ == "__main__":
    app.run(debug=True)