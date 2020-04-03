from flask import Flask, render_template      

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

'''    
@app.route("/worldmap")
def worldmap():
    return render_template("plots/global-coronavirus-cases.html")
'''
    
if __name__ == "__main__":
    app.run(debug=True)