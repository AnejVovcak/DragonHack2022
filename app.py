from flask import Flask, render_template
import os
import random
import threading
from vid import zaznavanje,izpis
app = Flask(__name__)


@app.route("/")
def index():
    return "to je osnovno stran ekipe Mavens!"

#URL naše glavne aplikacije
@app.route("/platno")
def platno():
    return render_template("platno.html")

@app.route("/analiza")
def analiza():
    return render_template("analiza.html")

#GET poizvedba, ki vrne podatke, ki jih zazna rač. vid
@app.route("/podatki", methods=["GET"])
def me_api():
    return izpis()

#funkcija, ki se pokliče v novem threadu, ob začetku aplikacije
def server():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
#funkcija, ki se pokliče ob začetku aplikacije
if __name__ == "__main__":

    #definiramo thread, ki bo poklical funkcijo zaznavanje (rač. vid)
    t1 = threading.Thread(target=zaznavanje)

    #definiramo glavni thread, ki bo poklical funkcijo server - zagon flask serverja
    t2=threading.Thread(target=server)
   
    t2.setDaemon(True)

    #najprej se zažene nov thread, ki bo poklical funkcijo zaznavanje (rač. vid)
    t1.start()

    #nato se zažene glavni thread, ki bo poklical funkcijo server - zagon flask serverja
    t2.start()
    t1.join()
    try:
       while True:
            pass
    except KeyboardInterrupt:
        print("Koncaj")
        exit()
   
   
   
