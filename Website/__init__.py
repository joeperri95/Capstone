#!/usr/bin/env python3.5

from flask import Flask, render_template, request, flash, send_file
from .server import *
import pickle
import os
import sys
import logging
import socket

HOST = 'localhost'
SENDPORT = 12345
RECVPORT = 12346



if __name__ == '__main__':

    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                        filename="server.log", level=logging.DEBUG)

    app = createApp()
    app.run(debug=True,host='0.0.0.0')
