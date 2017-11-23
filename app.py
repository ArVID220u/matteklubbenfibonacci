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


    #return render_template("home.html")
    return feed()

@app.route("/hmt")
def hmt():
    return redirect("https://goo.gl/forms/evYAz2VM5jaHnWlQ2")


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

def getproblemtitle(problemid):
    blogtitlepath = rlpt("static/problems/" + problemid + ".txt")
    problemtitle = problemid
    with open(blogtitlepath) as blogtitlefile:
        problemtitle = blogtitlefile.read()
    return problemtitle



# ABOUT

@app.route("/om")
def about():
    return render_template("about.html")


@app.route("/information")
def info():
    return render_template("info.html")





def getblogposttitle(blogid):
    blogtitlepath = rlpt("blog/" + blogid + "/title.txt")
    problemtitle = blogid
    with open(blogtitlepath) as blogtitlefile:
        problemtitle = blogtitlefile.read()
    return problemtitle



def addextradatatoblogpost(problemstatement, problemid):
    # all extra data is identified by being enclosed in %al% tags
    # thus, all elements on even indices are raw html code,
    # while all odd elements constitute some type of extra data
    problemstatementsplit = problemstatement.split("%al%")

    realproblemstatement = ""

    for index, data in enumerate(problemstatementsplit):
        # if index is even, just continue
        if index % 2 == 0:
            realproblemstatement += data
            continue

        # strip for whitespace in identifier part
        data = data.lstrip()


        if data.startswith("image"):
            # images are identified by %al%image:filename.png%al%
            filenamestring = data.split(":")[1].strip()
            # add an img tag. add an extra class that is this problems id concatenated with the filename (without extension), for custom styling
            realproblemstatement += "<img class='blogpostimage " + blogid + filenamestring.split('.')[0].split(' ')[0] + "' src='" + url_for('static', filename='blog/' + blogid + "/" + filenamestring) + "'>"

        elif data.startswith("problemlink"):
            # problemlink has format problemlink:problemid
            problemidstring = data.split(":")[1].strip()
            realproblemstatement += url_for("problem", problemid=problemidstring)

        elif data.startswith("problemtitle"):
            # formt problemlink:problemtitle
            problemidstring = data.split(":")[1].strip()
            realproblemstatement += getproblemtitle(problemidstring)

        elif data.startswith("link"):
            # format link:selector
            selectorstring = data.split(":")[1].strip()
            realproblemstatement += url_for(selectorstring, _external=True, _scheme="https")

        elif data.startswith("staticlink"):
            # format link:path
            selectorstring = data.split(":")[1].strip()
            realproblemstatement += url_for("static", filename=selectorstring, _external=True, _scheme="https")



    return realproblemstatement




@app.route("/flode")
def feed():
    blogids = os.listdir(rlpt("blog"))
    blogposts = []
    for blogid in blogids:
        if blogid.startswith("%"):
            continue
        post = {}
        post["blogid"] = blogid
        post["title"] = getblogposttitle(blogid)

        statementspath = rlpt("blog/" + blogid + "/content.html")
        blogstatement = "Tomt inlägg."
        if os.path.exists(statementspath):
            # load blog statement
            with open(statementspath) as statementfile:
                blogstatement = statementfile.read()


        datepath = rlpt("blog/" + blogid + "/date.txt")
        dat = datetime.now()
        # load date 
        with open(datepath) as datefile:
            datsr = datefile.read().strip()
            dat = datetime.strptime(datsr, "%Y-%m-%d %H:%M:%S.%f")
            post["realdate"] = dat

        # convert dat to the right format
        months = ["coolt", "januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"]
        post["date"] = str(dat.day) + " " + months[dat.month] + " " + str(dat.year)




        # maybe add images to the problem statement
        blogstatement = addextradatatoblogpost(blogstatement, blogid)

        post["content"] = blogstatement

        blogposts.append(post)

    # sort by date
    blogposts = sorted(blogposts, key=lambda k: k["realdate"], reverse=True)
    for b in blogposts:
        b.pop("realdate", None)

    return render_template("feed.html", blogposts=blogposts)



if __name__ == "__main__":
    app.run()
