#!/usr/bin/env python3.6

from flask import Flask, render_template, request, flash
import os
import logging

def createApp():
    app = Flask(__name__,static_url_path='/static')
    app.secret_key = "super secret key"

    @app.route('/', methods=["GET", "POST"])
    def mainRoute():

        if request.method == "POST":
            res = request.form

            print(res['firstname'])

            if res['firstname'] == '' or res['lastname'] == '':
                #make an error page
                flash("Bad")
                logging.error(f"Empty name field: {res['drink']},{res['firstname']},{res['lastname']},{res['station']}")

            elif res['drink'] == 'Drink':
                #make an error page
                flash("Bad")
                logging.error(f"Invalid drink order: {res['drink']},{res['firstname']},{res['lastname']},{res['station']}")


            elif res['station'] == 'Station':
                flash("Bad")
                logging.error(f"Invalid station order: {res['drink']},{res['firstname']},{res['lastname']},{res['station']}")

            else:
                logging.info(f"{res['drink']} order from {res['firstname']} {res['lastname']} at {res['station']}")
                flash("Good")

        return render_template('index.html')

    return app


if __name__ == '__main__':

    logging.basicConfig(format = "%(asctime)s %(levelname)s %(message)s", filename="server.log", level=logging.DEBUG)

    app = createApp()
    app.run(debug=True)
