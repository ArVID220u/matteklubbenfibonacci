#!/usr/bin/env python3
import random, os, sys, binascii
import subprocess
import sqlite3
from hashlib import md5
from base64 import b64encode
from datetime import datetime
import time
import config as turingconfig

# set timezone
os.environ["TZ"] = "Europe/Stockholm"

from flask import *
app = Flask(__name__)
app.config.from_object(__name__) # configure from this file
app.config["SECRET_KEY"] = turingconfig.FLASK_SECRET_KEY
#HTTPS
app.config["PREFERRED_URL_SCHEME"] = "https"

# apparently this is for safety of some sort
def rlpt(pt):
    return os.path.join(app.root_path, pt)

@app.route("/googled4987f8a6a3dfeee.html")
def authenticate_for_google():
    return "google-site-verification: googled4987f8a6a3dfeee.html"




def httpsify(url):
    if url.startswith("http://"):
        return url.replace("http://", "https://", 1)
    return url




@app.route("/")
def home():

    return render_template("home.html")


@app.route("/problem")
def problemslist():
    # list all problems
    problemids = reversed(sorted(os.listdir(rlpt("static/problems"))))
    problems = []
    for problemid in problemids:
        if problemid.startswith("%"):
            continue
        if problemid.endswith("pdf"):
            continue
        if not problemid.endswith(".txt"):
            continue
        problemtitle = "Något gick väldigt snett här."
        with open(rlpt("static/problems/" + problemid), "r") as tf:
                problemtitle = tf.read()
        problem = {}
        problem["filename"] = "problems/" + problemid[:-4] + ".pdf"
        problem["filetitle"] = problemtitle
        problems.append(problem)


    return render_template("problemslist.html", problems = problems)



# ABOUT

@app.route("/om")
def about():
    return render_template("about.html")


@app.route("/information")
def info():
    return render_template("info.html")



if __name__ == "__main__":
    app.run()
