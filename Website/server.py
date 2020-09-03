
from flask import Flask, render_template, request, flash, send_file
import pickle
import os
import sys
import logging
import socket

HOST = 'localhost'
SENDPORT = 12345
RECVPORT = 12346


def createApp():

    app = Flask(__name__, static_url_path='/static')
    app.secret_key = "super secret key"

    @app.route('/', methods=["GET", "POST"])
    def mainRoute():

        if request.method == "POST":
            res = request.form

            if res['firstname'] == '' or res['lastname'] == '':
                flash("Bad")
                logging.error("Empty name field: " + str(res['drink']) + "," + str(
                    res['firstname']) + "," + str(res['lastname']) + ',' + str(res['station']))

            elif res['drink'] == 'Drink':
                flash("Bad")
                logging.error("Invalid drink order: " + str(res['drink']) + "," + str(
                    res['firstname']) + "," + str(res['lastname']) + ',' + str(res['station']))

            elif res['station'] == 'Station':
                flash("Bad")
                logging.error("Invalid station order: " + str(res['drink']) + "," + str(
                    res['firstname']) + "," + str(res['lastname']) + ',' + str(res['station']))

            else:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((HOST, SENDPORT))
                    serialObject = pickle.dumps(res)
                    sock.send(serialObject)
                    sock.close()

                    logging.info(
                        str(res['drink']) + ' order from ' + str(res['firstname']) + ' ' + str(res['lastname']) + ' at ' + str(res['station']))
                    flash("Good")

                except ConnectionRefusedError as e:
                    logging.error(
                        "no socket found order will not be processed")
                    flash('No Server')

        return render_template('index.html', caption="The Next Generation Bar Experience.")

    @app.route('/about')
    def about():
        return render_template('about.html', title="About Us", caption="Learn More About Us!", teammates=teammates)

    @app.route('/track')
    def track():

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        res = ""
        try:

            sock.bind((HOST, RECVPORT))
            sock.listen(5)

            conn, addr = sock.accept()

            while(1):

                data = conn.recv(1024)

                if(data):
                    serialObject = pickle.loads(data)
                else:
                    break

            sock.close()
        except TimeoutError as e:
            pass
        finally:
            print (serialObject)
            return render_template('track.html', title="Current", caption="Now Serving",orders=serialObject)
            sock.close()

    @app.route('/project')
    def project():
        return send_file('static/AboutProject.pdf')

    return app


teammates = [
    {
        'Name': 'Maharshi Patel',
        'Bio': 'Maharshi is a Electrical B.Eng candidate at McMaster University. In this project he developed the dispension system and the HMI. He also worked on group administration. He hopes that his contributions in this project will lead to new career oportunities.',
        'Task1': 'Drink Dispension System',
        'Task2': 'Human Machine Interface',
        'Task3': 'Group Administration',
        'LinkedIn': 'https://www.linkedin.com/in/maharshipatel1997/',
        'Img': "static/Maharshi.jpg",
    },
    {
        'Name': 'Malcolm MacEachern',
        'Bio': 'Malcolm is a graduating Electrical Engineer who was the main structural lead for this project, as well as assisting with aspects of dispension and locomotion sub-systems. He is looking forward to working on projects related to the fields of robotics & automation.',
        'Task1': 'Structural Design/Simulation',
        'Task2': 'Robot Assembly',
        'Task3': 'General Engineering',
        'LinkedIn': 'https://www.linkedin.com/in/malcolm-maceachern-6b2624116/',
        'Img': "static/Malcolm.jpeg",
    },
    {
        'Name': 'Joe Perri',
        'Bio': 'Joe is an aspiring embedded systems engineer who worked on the firmware for the project, helping with the HMI, the overall logic and controls systems. This project acted as a great opportunity to expand his experience in software design and image processing.',
        'Task1': 'Navigation',
        'Task2': 'Supervisory Logic',
        'Task3': 'Multithreading',
        'Git': 'https://github.com/joeperri95/',
        'Img': "static/Joe.png"
    },
    {
        'Name': 'Paul Nguyen',
        'Bio': 'Paul is a B. Eng candidate at McMaster University. His technical contribution on the team focuses on the locomotion system. As a result of his involvement on the project, he wishes to pursue advance studies in motor design, inverter design and motor controls.',
        'Task1': 'Locomotion',
        'Task2': 'Power Systems',
        'Task3': 'General Engineering',
        'Img': "static/Random.jpeg"
    }
]