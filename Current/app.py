from flask import Flask, render_template      

app = Flask(__name__)

@app.route("/")
def globe_map():
    return render_template("globe-page.html")

@app.route("/globe_map")
def globe_map_copy():
    return render_template("globe-page.html")

    
@app.route("/coronavirus_bubble_map")
def coronavirus_bubble_map():
    return render_template("bubble-map-page.html")

@app.route("/us_state_map")
def us_state_map():
    return render_template("us-state-map-page.html")

    
if __name__ == "__main__":
    app.run(debug=True)