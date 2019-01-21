#!/usr/bin/env python3.6

from flask import Flask, render_template, request
import os
import logging

def createApp():
    app = Flask(__name__,static_url_path='/static')

    @app.route('/', methods=["GET", "POST"])
    def mainRoute():

        if request.method == "POST":
            res = request.form
            
            if res['firstname'] is None or res['lastname'] is None:
                #make an error page
                logging.error(f"Empty name field: {res['drink']},{res['firstname']},{res['lastname']},{res['station']}")
                return 'error'

            if res['drink'] == 'Drink':
                #make an error page
                logging.error(f"Invalid drink order: {res['drink']},{res['firstname']},{res['lastname']},{res['station']}")
                return 'error' 


            if res['station'] == 'Station':
                logging.error(f"Invalid station order: {res['drink']},{res['firstname']},{res['lastname']},{res['station']}")
                return 'error'


            logging.info(f"{res['drink']} order from {res['firstname']} {res['lastname']} at {res['station']}")

        return render_template('index.html')

    return app


if __name__ == '__main__':
    
    logging.basicConfig(format = "%(asctime)s %(levelname)s %(message)s", filename="server.log", level=logging.DEBUG)
    
    app = createApp()
    app.run()