from flask import Flask, render_template
import os
import random
from vid import izpis
app = Flask(__name__)

@app.route("/")
def index():
    url = "../img/slika1.jpg"
    return render_template("index.html", url=url)
    #return "halo halo"

@app.route("/test")
def index1():
   return "halo halo"

@app.route("/platno")
def platno():
    me = me_api()
    print(me)
    url = None
    return render_template("platno.html", url=url)

@app.route("/me", methods=["GET"])
def me_api():
    return izpis()
    
if __name__ == "__main__":
   app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
 