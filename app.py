import base64
import calendar
import datetime
import io
import logging
# import StringIO
from bson import ObjectId
import os
from turtle import update
import pymongo
import time
from tempfile import mkdtemp
from typing import Text
from PIL import Image
import base64

from cs50 import SQL
from flask_session import Session

from werkzeug.exceptions import (HTTPException, InternalServerError,
                                 default_exceptions)
from werkzeug.security import check_password_hash, generate_password_hash

from flask import (Flask, Response, flash, redirect, render_template, request,
                   session)
from helpers import apology, login_required, lookup, usd
from logginner import loginner

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


path = '/Users/niroren/Desktop/temp.png'


def isAdmin():
    user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
    if user['admin'] != 1:
        return redirect('/')
    
    return True
    
def isCoder():
    user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
    if user['admin'] != 2:
        return redirect('/')
    return True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://niroren:Sisma1234@coportal.ewqeptv.mongodb.net/test"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = pymongo.MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['coportal']

db = get_database()
COLLEGES = db['colleges']
USERS = db['users']
LOGINS = db['logins']
CHECKLISTS = db['checklists']

def coco():
    all_colleges = open('/Users/niroren/Documents/CollegePortal/all_colleges.csv', 'r').readlines()
    colleges = []
    for i in all_colleges:
        i= i.split('	')
        i[1]=i[1].replace(' iversity', ' University')
        colleges.append(i[1])
    return colleges


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        checklists = []
        logins = list(LOGINS.find({'userID' : ObjectId(session['user_id'])}))
        # db.execute("SELECT * FROM logins WHERE userID = ?", session['user_id'])
        for login in logins:
            checklist = {}
            # for each login create a table with all the details
            collegeID = login['collegeID']
            collegeInfo = list(COLLEGES.find({'_id' : ObjectId(collegeID)}))
            # db.execute(
            #     "SELECT * FROM colleges WHERE collegeID = ?", 
            #     collegeID
            #     )
            if len(collegeInfo) ==0:
                flash('new college')
                collegeName = 'NONE YET'
                collegeURL = 'NONE YET'
            else:
                collegeName = collegeInfo[0]['name']
                collegeURL = collegeInfo[0]['url']
            checklist['collegeName'] = collegeName
            checklist['collegeURL'] = collegeURL
            details = list(CHECKLISTS.find({'userID' : ObjectId(session['user_id']), 'collegeID' : collegeID}))
            # db.execute(
            #     "SELECT * FROM checklist WHERE userID = ? and collegeID = ?", 
            #     session['user_id'],
            #     collegeID
            #     )
            checklist['details'] = details
            checklists.append(checklist)
        return render_template("index.html", checklists= checklists)
    else:
        checklists = []
        logins = list(LOGINS.find({'userID' : ObjectId(session['user_id'])}))
        # db.execute("SELECT * FROM logins WHERE userID = ?", session['user_id'])
        for login in logins:
            checklist = {}
            # for each login create a table with all the details
            collegeID = login['collegeID']
            collegeInfo = list(COLLEGES.find({'_id' : collegeID}))
            # db.execute(
            #     "SELECT * FROM colleges WHERE collegeID = ?", 
            #     collegeID
            #     )
            
            if len(collegeInfo) ==0:
                flash('new college')
                collegeName = 'NONE YET'
                collegeURL = 'NONE YET'
            else:
                collegeName = collegeInfo[0]['name']
                collegeURL = collegeInfo[0]['url']
            checklist['collegeName'] = collegeName
            checklist['collegeURL'] = collegeURL
            details = list(CHECKLISTS.find({'userID' : ObjectId(session['user_id']), 'collegeID' : collegeID}))
            # db.execute(
            #     "SELECT * FROM checklist WHERE userID = ? and collegeID = ?", 
            #     session['user_id'],
            #     collegeID
            #     )
            checklist['details'] = details
            checklists.append(checklist)

        return render_template("index.html", checklists = checklists) 



@app.route("/admin/adminhome", methods=["GET", "POST"])
@login_required
def adminhome():
    if request.method == "POST":
        flash("entered successfully")
        return render_template("adminhome.html")
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        if user['admin'] == 0:
            return redirect('/')
        return redirect('/admin/searchProfile')

@app.route("/coder/coderhome", methods=["GET", "POST"])
@login_required
def coderhome():
    if request.method == "POST":
        collegeID = request.args.get('collegeID', default=0, type=int)
        COLLEGES.update_one({'_id' : ObjectId(COLLEGEID)},update = {'$set' : {'loginworks' : 1}})
        # db.execute("UPDATE colleges SET loginworks = ? WHERE collegeID = ?", 1, COLLEGEID)
        flash("entered successfully")
        return render_template("coderhome.html")
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        if user['admin'] != 2:
            return redirect('/')

        todoColleges = list(COLLEGES.find({'loginworks' : 0}))
        # db.execute(
        #         "SELECT * FROM colleges WHERE loginworks = ?", 
        #         0
        #         )
        table = []
        for college in todoColleges:
            row = {}
            name = college['name']
            id = college['collegeID']
            row['collegeName'] = name
            row['collegeID'] = id
            url = '/coder/coderhome?collegeID=' + str(id)
            
            row['url'] = url
            table.append(row)
        return render_template("coderhome.html", table = table)


@app.route("/admin/geturl", methods=["GET", "POST"])
@login_required
def geturl():
    if request.method == "POST":
        flash("entered successfully")
        return render_template("adminTest.html")
    else:

        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))
        if user[0]['admin'] == 0:
            flash('not an admin')
            return redirect('/')

        if user[0]['admin'] == 1:
            todoColleges = list(COLLEGES.find({'url' : 'TODO'}))
            # db.execute(
            #     "SELECT * FROM colleges WHERE url = ?", 
            #     'TODO'
            #     )
            table = []
            for college in todoColleges:
                row = {}
                name = college['name']
                id = college['_id']
                row['collegeName'] = name
                row['collegeID'] = id
                url = '/admin/addurlcollege?collegeID=' + str(id)
                
                row['url'] = url
                table.append(row)
            return render_template("geturl.html", table = table)


COLLEGEID = 0

@app.route("/admin/addurlcollege", methods=["GET", "POST"])
@login_required
def addurlcollege():
    global COLLEGEID
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            flash("must provide url")
        
        COLLEGES.update_one({'_id' : ObjectId(COLLEGEID)},update = {'$set' : {'url' : url}})
        # db.execute("UPDATE colleges SET url = ? WHERE collegeID = ?", url, COLLEGEID)
        flash("entered successfully")
        return redirect("/admin/confirmurl")
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        if user['admin'] == 0:
            return redirect('/')

            
        collegeID = request.args.get('collegeID', default=0, type=str)
        COLLEGEID = collegeID
        collegeInfo = list(COLLEGES.find({'_id' : ObjectId(collegeID)}))
        # db.execute(
        #         "SELECT * FROM colleges WHERE collegeID = ?", 
        #         collegeID
        #         )
        name = collegeInfo[0]['name']
        return render_template("addurlcollege.html",name = name)

@app.route("/admin/confirmurl", methods=["GET", "POST"])
@login_required
def confirmurl():
    global COLLEGEID
    if request.method == "POST":
        #TODO!!!!!
        works = request.form.get("works")
        if not works:
            flash("must provide url")
        if works == 'No':
            works = 0
        elif works == 'Yes':
            works = 1
        COLLEGES.update_one({'_id' : ObjectId(COLLEGEID)},update={'$set':{'urlworks' : works}})
        # db.execute("UPDATE colleges SET urlworks = ? WHERE collegeID = ?", works, COLLEGEID)
        flash("entered successfully")
        return render_template("geturl.html")
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        if user['admin'] == 0:
            return redirect('/')

            
        first_login = list(COLLEGES.find({'_id' : ObjectId(COLLEGEID)}))
        # db.execute(
        #         "SELECT * FROM logins WHERE collegeID = ?", 
        #         COLLEGEID
        #         )
        url = list(COLLEGES.find({'_id' : ObjectId(COLLEGEID)}))[0]['url']
        password = first_login[0]['password']
        email = first_login[0]['email']
        converted_image = loginner(url, email,password)

        #TODO
        #I NEED TO INSERT THE CONVERTED IMAGE INTO THE DATABASE, INTO THE LOGIN TABLE TO THE LOGIN
        #THEN I NEED TO PASS SOMETHING DISPLAYABLE INTO CONVERTED IMAGE
        return render_template("confirmurl.html",page_source = converted_image)

@app.route("/admin/changedlogins", methods=["GET", "POST"])
@login_required
def changedlogins():
    if request.method == "POST":
        return render_template("changedlogins.html")
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        if user['admin'] == 0:
            return redirect('/')

            
        logins = list(LOGINS.find({'changed' : 1}))
        # db.execute("SELECT * FROM logins WHERE changed = ?", 1)
        for login in logins:
            print('need to make buttons and shit')
        


        return render_template("changedlogins.html")


@app.route("/admin/viewProfile", methods=["GET", "POST"])
@login_required
def viewProfile():
    if request.method == "POST":
        return render_template()
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        # db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])[0]
        if user['admin'] == 0:
            return redirect('/')

            
        userID = request.args.get('userID', default=0, type=str)
        # print('userID', userID)
        checklists = []
        logins = list(LOGINS.find({'userID' : ObjectId(userID)}))

        # db.execute("SELECT * FROM logins WHERE userID = ?", userID)
        for login in logins:
            checklist = {}
            # for each login create a table with all the details
            collegeID = login['collegeID']
            collegeInfo = list(COLLEGES.find({'_id' : ObjectId(collegeID)}))
            # db.execute(
            #     "SELECT * FROM colleges WHERE collegeID = ?", 
            #     collegeID
            #     )
            
            collegeName = collegeInfo[0]['name']  
            collegeID = collegeInfo[0]['_id']

            checklist['collegeName'] = collegeName
            checklist['editURL'] = '/admin/editDetails?userID='+str(userID)+'&collegeID='+str(collegeID)
            print('US', userID)
            print('ID', collegeID)
            details = list(CHECKLISTS.find({'userID' : ObjectId(userID),'collegeID' : (collegeID)}))

            # db.execute(
            #     "SELECT * FROM checklist WHERE userID = ? and collegeID = ?", 
            #     userID,
            #     collegeID
            #     )
            checklist['details'] = details
            checklists.append(checklist)
        return render_template("viewProfile.html", checklists = checklists)

addDetail_userID = 0
addDetail_collegeID = 0
@app.route("/admin/addDetail", methods=["GET", "POST"])
@login_required
def addDetail():
    global addDetail_userID
    global addDetail_collegeID
    if request.method == "POST":
        detail = request.form.get("detail")
        status = request.form.get("status")
        date = request.form.get("date")
        
        for_insert = {
            'userID' : ObjectId(addDetail_userID),
            'collegeID':ObjectId(addDetail_collegeID),
            'detail':detail,
            'status':status,
            'date':date
        }
        CHECKLISTS.insert_one(for_insert)
        # db.execute('INSERT INTO checklist (userID, collegeID, detail, status, date) VALUES(?,?,?,?,?)',
        #     addDetail_userID,
        #     addDetail_collegeID,
        #     detail,
        #     status,
        #     date)
        flash('added')
        return redirect('/admin/editDetails?userID='+str(addDetail_userID)+'&collegeID='+str(addDetail_collegeID))
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        if user['admin'] == 0:
            return redirect('/')

            
        userID = request.args.get('userID', default=0, type=str)
        addDetail_userID = userID
        collegeID = request.args.get('collegeID', default=0, type=str)
        addDetail_collegeID = collegeID
        viewURL = '/admin/viewPortal?userID='+str(userID)+'&collegeID='+str(collegeID)
        return render_template("addDetail.html", viewURL = viewURL)

@app.route("/admin/viewPortal", methods=["GET", "POST"])
@login_required
def viewPortal():
    if request.method == "POST":
        return render_template("viewPortal.html")
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        if user['admin'] == 0:
            return redirect('/')

            
        userID = request.args.get('userID', default=0, type=int)
        collegeID = request.args.get('collegeID', default=0, type=int)
        login = (LOGINS.find({'userID' : userID, 'collegeID' : collegeID}))[0]
        # db.execute("SELECT * FROM logins WHERE userID = ? and collegeID=?", userID, collegeID)[0]
        email = login['email']
        password = login['password']
        college = list(COLLEGES.find({'_id' : ObjectId(collegeID)}))[0]
        # db.execute("SELECT * FROM colleges WHERE collegeID=?", collegeID)[0]
        url = college['url']
        converted_image = loginner(url, email,password)

        LOGINS.update_one({'userID':userID,'collegeID':collegeID}, update={'$set':{'pageSource' : converted_image}})
        # db.execute("update logins set pageSource=?WHERE userID = ? and collegeID=?", converted_image,userID, collegeID)
        
        return render_template("viewPortal.html", converted_image = converted_image)

@app.route("/admin/searchResults", methods=["GET", "POST"])
@login_required
def searchResults():
    if request.method == "POST":
        return render_template("searchResults.html")
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        if user['admin'] == 0:
            return redirect('/')

            
        return render_template("searchResults.html")
    


@app.route("/admin/searchProfile", methods=["GET", "POST"])
@login_required
def searchProfile():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        userID = request.form.get("userID")

        if name and not email and not userID:
            users = list(USERS.find({'name' : name}))

        elif email and not name and not userID:
            users = list(USERS.find({'email' : email}))

        elif userID and not email and not name:
            users = list(USERS.find({'_id' : ObjectId(userID)}))

        elif name and email and not userID:
            users = list(USERS.find({'name' : name,'email':email}))
            
        elif name and userID and not email:
            users = users = list(USERS.find({'name' : name,'_id':ObjectId(userID)}))
           
        elif userID and email and not name:
            users = users = list(USERS.find({'_id' : ObjectId(userID),'email':email}))
            
        elif userID and email and name:
            users = list(USERS.find({'name' : name,'email':email,'_id' : ObjectId(userID)}))
            
        for user in users:
            user['url'] = '/admin/viewProfile?userID=' + str(user['_id'])
            print(user['url'])
            print('SS user ID : ',str(user['_id']))
        
        return render_template("searchResults.html", users=users)
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        # db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])[0]
        if user['admin'] == 0:
            return redirect('/')

            
        userID = request.args.get('userID', default=0, type=int)
        collegeID = request.args.get('collegeID', default=0, type=int)
        details = (CHECKLISTS.find({'userID' : userID,'collegeID':collegeID}))
        # db.execute("SELECT * FROM checklist WHERE userID = ? and collegeID=?", userID, collegeID)
        addURL = '/admin/addDetail?userID='+str(userID)+'&collegeID='+str(collegeID)
        return render_template("searchProfile.html", details= details,addURL=addURL)

editDetails_userID = 0
editDetails_collegeID = 0
@app.route("/admin/editDetails", methods=["GET", "POST"])
@login_required
def editDetails():
    global editDetails_collegeID
    global editDetails_userID
    if request.method == "POST":
        details = list(CHECKLISTS.find({'userID' : ObjectId(editDetails_userID), 'collegeID' : ObjectId(editDetails_collegeID)}))
        # db.execute("SELECT * FROM checklist WHERE userID = ? and collegeID=?", editDetails_userID, editDetails_collegeID)
        for i in details:
            id = str(i['_id'])
            print(id)
            print('det',request.form.get(str(id)+'detail'))
            CHECKLISTS.update_one({'_id' : ObjectId(id)},update ={'$set':{'detail' : request.form.get(str(id)+'detail')}})
            # db.execute("update checklist set detail=?WHERE checkID=?", request.form.get(str(id)+'detail'),id)
            CHECKLISTS.update_one({'_id' : ObjectId(id)},update ={'$set':{'status' : request.form.get(str(id)+'status')}})
            # db.execute("update checklist set status=?WHERE checkID=?", request.form.get(str(id)+'status'),id)
            CHECKLISTS.update_one({'_id' : ObjectId(id)},update ={'$set':{'date' : request.form.get(str(id)+'date')}})
            # db.execute("update checklist set date=?WHERE checkID=?", request.form.get(str(id)+'date'),id)
        flash('saved')
        return redirect('/admin/editDetails?userID='+str(editDetails_userID)+'&collegeID='+str(editDetails_collegeID))
    else:
        user = list(USERS.find({'_id' : ObjectId(session['user_id'])}))[0]
        # db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])[0]
        if user['admin'] == 0:
            return redirect('/')


        userID = request.args.get('userID', default=0, type=str)
        editDetails_userID = userID
        collegeID = request.args.get('collegeID', default=0, type=str)
        editDetails_collegeID = collegeID
        print('1',editDetails_collegeID)
        print('2',editDetails_userID)
        details = list(CHECKLISTS.find({'userID' : ObjectId(userID),'collegeID': ObjectId(collegeID)}))
        for d in details:
            d['_id'] = str(d['_id'])
        # db.execute("SELECT * FROM checklist WHERE userID = ? and collegeID=?", userID, collegeID)
        addURL = '/admin/addDetail?userID='+str(userID)+'&collegeID='+str(collegeID)
        viewURL = '/admin/viewPortal?userID='+str(userID)+'&collegeID='+str(collegeID)

        return render_template("editDetails.html", details= details,addURL=addURL, viewURL = viewURL)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("email"):
            flash("must provide email")
            return render_template("login.html")
        elif not request.form.get("password"):
            flash("must provide password")
            return render_template("login.html")
        rows = list(USERS.find({'email' : request.form.get("email")}))
        # db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid email and/or password")
            return render_template("login.html")
            #return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = str(rows[0]["_id"])

        # Redirect user to home page
        if rows[0]['admin'] ==0:
            return redirect("/")
        elif rows[0]['admin'] ==1:
            return redirect('/admin/adminhome')
        elif rows[0]['admin'] ==2:
            return redirect('/coder/coderhome')

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        repassword = request.form.get('confirmation')
        name = request.form.get('name')
        year = request.form.get('year')
        if not email:
            flash("must provide email")
            return render_template("register.html")
        elif not password:
            flash("must provide password")
            return render_template("register.html")
        elif repassword is None:
            flash("must retype password")
            return render_template("register.html") 
        elif name is None:
            flash("must provide name")
            return render_template("register.html")
        elif year is None:
            flash("must provide year")
            return render_template("register.html")
        if password != repassword:
            flash("passwords must match")
            return render_template("register.html")
        
        rows = list(USERS.find({'email' : email}))
        # db.execute("SELECT * FROM users WHERE email = ?", email)
        if len(rows) != 0:
            flash("email exists in system")
            return render_template("register.html")
        else:
            hashed_password = generate_password_hash(password)
            profile = {
                'email':email,
                'hash':hashed_password,
                'name':name,
                'year':year,
                'admin':0,
            }
            USERS.insert_one(profile)
            # db.execute('INSERT INTO users (email, hash, name, applicationYear, admin) VALUES(?,?,?,?,?)',
            # email,
            # hashed_password,
            # name,
            # year,
            # 0)

            return redirect('/')

    else:
        return render_template("register.html")


@app.route("/addcollege", methods=["GET", "POST"])
@login_required
def addcollege():
    if request.method == "POST":
        collegeName = request.form.get('collegeName')
        username = request.form.get('username')
        password = request.form.get('password')
        if not collegeName:
            flash("must provide a collegeName")
            return render_template("addcollege.html")
        elif not username:
            flash("must provide a description")
            return render_template("addcollege.html")
        elif not password:
            flash("must provide a password")
            return render_template("addcollege.html")
        

        college = list(COLLEGES.find({'name':collegeName}))
        # db.execute("SELECT * FROM colleges where name = ?", collegeName)
        if len(college) == 0:
            c = {
                'name': collegeName,
                'url' : 'TODO',
                'urlworks' : 0,
                'loginworks' : 0
            }
            COLLEGES.insert_one(c)
            # db.execute('INSERT INTO colleges (name, url, urlworks,loginworks) VALUES(?,?,?,?)',
            # collegeName,
            # 'TODO',
            # 0,0
            # )

            college = list(COLLEGES.find({'name':collegeName}))
            # db.execute(
            #     "SELECT * FROM colleges where name = ?", 
            #     collegeName
            #     )
            collegeID = college[0]['_id']
        else:
            collegeID = college[0]['_id']
        
        logins = list(LOGINS.find({'userID': ObjectId(session['user_id']), '_id' : ObjectId(collegeID)}))
        # db.execute("SELECT * FROM logins WHERE userID = ? and collegeID=?", session['user_id'], collegeID,)
        if len(logins) != 0:
            flash('college already added')
            return render_template("addcollege.html")
        l = {
            'userID' : ObjectId(session["user_id"]),
            'collegeID': collegeID,
            'email' : username,
            'password' : password,
            'changed' : 1,
            'pageSource' : 'None',
            'decisionOut' : 0
        }        

        LOGINS.insert_one(l)
        # db.execute('INSERT INTO logins (userID, collegeID, email, password, changed, pageSource) VALUES(?,?,?,?,?,?)',
        #     session["user_id"],
        #     collegeID,
        #     username,
        #     password,
        #     1,
        #     'None'
        #     )
        flash("added")
        return redirect('/')
    else:
        collegeList = coco()
        
       
        return render_template("addcollege.html", collegeList = collegeList)



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
