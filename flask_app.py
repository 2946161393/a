import pymysql
from flask import Flask, render_template
from flask.globals import request
import datetime


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("poll_home_page.html")


@app.route('/addpoll', methods=["get"])
def render_add_poll_form():
    return render_template("add_poll_form.html")

@app.route('/adduser', methods=["get"])
def render_add_user_form():
    return render_template("add_user_form.html")

@app.route('/deletepoll', methods=["get"])
def render_delete_poll_form():
    return render_template("delete_poll.html")

@app.route('/deleteuser', methods=["get"])
def render_delete_user_form():
    return render_template("delete_user.html")

@app.route('/addpollenrollment', methods=["get"])
def render_add_pollenrollment_form():
    return render_template("add_pollenrollment_form.html")

# Simply returns the form to fill out a form to get enrollment data
@app.route('/pollenrollment', methods=["get"])
def render_get_pollenrollment_form():
    return render_template("get_pollenrollment_form.html")

@app.route('/poll', methods=["get"])
def render_poll_form():
    return render_template("poll.html")

@app.route('/login', methods=["get"])
def render_login_form():
    return render_template("login.html")


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template(login.html)

    loginname = request.values["loginname"]
    password = request.values["loginpassword"]
    dbconnection = getdbconnection(mysqlconnection)
    dbcursor = None
    try:
        dbcursor = dbconnection.cursor()
        sql_query = "SELECT * FROM user WHERE username = %s and password = %s"
        dbcursor.execute(sql_query,(loginname, password))
        user= dbcursor.fetchone()
        if user is not None:
            return "<h1>User " + loginname + " logged in</h1>"
        else:
            return "<h1>User " + loginname + " is not authorized!</h1>"
    finally:
        if dbcursor is not None:
            dbcursor.close()

        
# This view function adds a poll to the poll database table.
@app.route("/addnewpoll", methods=["post"])
def add_new_poll():
    dbConnection = getdbconnection(mysqlconnection)
    dbcursor = None
    try:

        pollId = request.form.get('pollId')
        polltitle = request.form.get('polltitle')
        pollquestion = request.form.get('pollquestion')
        numOfchoice = request.form.get('numOfchoice')
        answertimes = request.form.get('answertimes')


        # Next, insert a row into the student DB table.
        dbcursor = dbConnection.cursor()
        insert_poll_qry = "INSERT INTO poll (pollId,polltitle,pollquestion,numOfchoice,answertimes) \
                                            VALUES (%s, %s, %s, %s, %s);"

        dbcursor.execute(insert_poll_qry, (pollId, polltitle, pollquestion, numOfchoice, answertimes))

        # connection is not autocommit by default. So you must commit to save your changes.
        # Do this after inserts, updates, and deletes.  In other words, any operation that
        # changes the state of the DB.  Select statements do not require this step.
        dbConnection.commit()

        # Build a response HTML document for confirmation
        html_response_str = render_template("added_poll.html", pollId = pollId, polltitle = polltitle,
                                    pollquestion = pollquestion, numOfchoice = numOfchoice, answertimes = answertimes)
    finally:
        if dbcursor is not None:
            dbcursor.close()

    return html_response_str


@app.route("/addnewuser", methods=["post"])
def add_new_user():
    dbConnection = getdbconnection(mysqlconnection)
    dbcursor = None
    try:
        userid = request.form.get('userid')
        password = request.form.get('password')
        fname = request.form.get('fname')
        mi = request.form.get('mi')
        lname = request.form.get('lname')
        usertype = request.form.get('usertype')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        address = request.form.get('address')
        phone = request.form.get('phone')


        # Next, insert a row into the student DB table.
        dbcursor = dbConnection.cursor()
        insert_user_qry = "INSERT INTO user (userid, password, fname, mi, lname, usertype, birthday, email, address, phone) \
                                            VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s);"

        dbcursor.execute(insert_user_qry, (userid, password, fname, mi, lname, usertype, birthday, email, address, phone))

        # connection is not autocommit by default. So you must commit to save your changes.
        # Do this after inserts, updates, and deletes.  In other words, any operation that
        # changes the state of the DB.  Select statements do not require this step.
        dbConnection.commit()

        # Build a response HTML document for confirmation
        html_response_str = render_template("added_user.html",  userid = userid, password = password,
                                    fname = fname, mi = mi, lname = lname, usertype = usertype, birthday = birthday, 
                                    email = email, address = address, phone = phone)
    finally:
        if dbcursor is not None:
            dbcursor.close()

    return html_response_str

@app.route("/removedpoll", methods=["post"])
def delete_poll():
    dbConnection = getdbconnection(mysqlconnection)
    dbcursor = None
    try:
        # First of all, read in the poll information from the HTML form filled out in the browser.
        pollId = request.form.get('pollId')


        # Next, delete the poll
        dbcursor = dbConnection.cursor()
        delete_poll_qry = "DELETE FROM poll \
                             WHERE (pollId = %s);"

        record_count = dbcursor.execute(delete_poll_qry, (pollId))

        dbConnection.commit()

        # Build a response HTML document for confirmation
        html_response_str = render_template("deleted_poll.html",
                                            record_count = record_count,
                                            pollId = pollId)
    finally:
        if dbcursor is not None:
            dbcursor.close()

    return html_response_str


@app.route("/removeduser", methods=["post"])
def delete_user():
    dbConnection = getdbconnection(mysqlconnection)
    dbcursor = None
    try:
        # First of all, read in the user information from the HTML form filled out in the browser.
        userid = request.form.get('userid')


        # Next, delete the user
        dbcursor = dbConnection.cursor()
        delete_user_qry = "DELETE FROM user \
                             WHERE (userId = %s);"

        record_count = dbcursor.execute(delete_user_qry, (userid))

        dbConnection.commit()

        # Build a response HTML document for confirmation
        html_response_str = render_template("deleted_user.html",
                                            record_count = record_count,
                                            userid = userid)
    finally:
        if dbcursor is not None:
            dbcursor.close()

    return html_response_str

# This view function adds a student to the enrollment database table.
@app.route("/addnewpollenrollment", methods=["post"])
def add_new_enrollment():
    dbConnection = getdbconnection(mysqlconnection)
    dbcursor = None
    try:
        userid = request.form.get('userid')
        userid = userid.strip()
     
        pollId = request.form.get('pollId')
        pollId = pollId.strip()

        if not doesUserExist(userid):
            msg = "User with userID of " + userid + " does not exist"
            return render_template("error_pollenrollment.html",
                                   userid=userid,
                                   pollId=pollId,
                                   error_message=msg)

        if not doesPollExist(pollId):
            msg = "Poll with ID of " + pollId +  " does not exist"
            return render_template("error_pollenrollment.html",
                                   userid=userid,
                                   pollId=pollId,
                                   error_message=msg)

        # Next, insert a row into the enrollment DB table.
        dbcursor = dbConnection.cursor()
        insert_pollenrollment_qry = "INSERT INTO pollenrollment \
                                (userid, pollId, dateRegistered) \
                                VALUES (%s, %s, %s);"
        dateRegistered = datetime.datetime.now().date()
        dateRegisteredStr = str(dateRegistered)
        dbcursor.execute(insert_pollenrollment_qry, (userid, pollId, dateRegisteredStr))

        # connection is not autocommit by default. So you must commit to save your changes.
        # Do this after inserts, updates, and deletes.  In other words, any operation that
        # changes the state of the DB.  Select statements do not require this step.
        dbConnection.commit()

        # Build a response HTML document for confirmation
        html_response_str = render_template("added_user_enrollment.html", userid=userid, pollId=pollId)
    finally:
        if dbcursor is not None:
            dbcursor.close()

    return html_response_str


@app.route('/poll', methods=['GET'])
def poll_question():
    if request.method =='GET':
        yes = request.args.get("selection")
        no = request.args.get("selection")
        other = request.args.get("selection")
    else:
        # This is how we read off an input value from a POST request.  Here
        # "word_to_check is the name of the input variable defined in the
        # HTML form
        yes = request.form.get("word_to_check")
        no = request.form.get("word_to_check")
        other = request.form.get("word_to_check")
    yes = yes.strip()
    no = no.strip()
    other = yes.strip()

    if yes:
        return '<h1> {} was your answer</h1>'.format(yes)
        # Return an HTML document.  It does not need to be complete.
    return '<h1>{} was your answer</h1>'.format(yes)
   
    if no:
        return '{} was your answer</h1>'.format(no)
    return '{} was your answer</h1>'.format(no)


    if other:
        return '{} was your answer</h1>'.format(no)
    return '{} was your answer</h1>'.format(other)


@app.route("/listpolls", methods=["get", "post"])
def list_polls():
    dbConnection = getdbconnection(mysqlconnection)
    dbcursor = None
    try:
        dbcursor = dbConnection.cursor()
        sql_query = "SELECT * from poll"
        recordCount = dbcursor.execute(sql_query)
        print("The query returns ", recordCount, " records.")
        result = dbcursor.fetchall()

        # This is for logging the result in Web Server log file.
        for pollRecord in result:
            print("ID: ", pollRecord[0],
                  ", polltitle: ", pollRecord[1],
                  ", numOfchoice: ", pollRecord[3])

        html_response_str = render_template("poll_list.html", poll_list = result)
    finally:
        if dbcursor is not None:
            dbcursor.close()

    return html_response_str

@app.route("/listusers", methods=["get", "post"])
def list_users():
    dbConnection = getdbconnection(mysqlconnection)
    dbDictionaryCursor = None
    try:
        dbDictionaryCursor = dbConnection.cursor(pymysql.cursors.DictCursor)
        sql_query = "SELECT * from user"
        recordCount = dbDictionaryCursor.execute(sql_query)
        print("The query returns ", recordCount, " records.")
        result = dbDictionaryCursor.fetchall()

        # This is for logging the result in Web Server log file.
        for userRecord in result:
            print("userId: ", userRecord['userid'],
                  ", First name: ", userRecord['fname'],
                  ", Last Name: ", userRecord['lname'])

        html_response_str = render_template("user_list.html", user_list = result)
    finally:
        if dbDictionaryCursor is not None:
            dbDictionaryCursor.close()

    return html_response_str

@app.route("/listpollenrollments", methods=["get", "post"])
def list_pollenrollments():
    dbConnection = getdbconnection(mysqlconnection)
    dbcursor = None
    try:
        userid = request.form.get('userid')
        userid = userid.strip()
        get_user_query = "SELECT fname, lname FROM user WHERE userid = %s"
        dbcursor = dbConnection.cursor()
        recordCount = dbcursor.execute(get_user_query, (userid))
        result = dbcursor.fetchone()
        if result != None:
            fname = result[0]
            lname = result[1]
            list_enrolled_poll_query = "SELECT * FROM pollenrollment WHERE userid = %s"
            dbcursor = dbConnection.cursor()
            recordCount = dbcursor.execute(list_enrolled_poll_query, (userid))
            print("The query returns ", recordCount, " records.")

            result = dbcursor.fetchall()
            # This is for logging the result in Web Server log file.
            for pollenrollmentRecord in result:
                print(pollenrollmentRecord)
                print("UserID: ", pollenrollmentRecord[0], ", poll ID: ", pollenrollmentRecord[1],
                      ", Date Registered: " , pollenrollmentRecord[2])

            html_response_str = render_template("enrolled_poll_list.html",
                                                fname = fname,
                                                lname= lname,
                                                enrolled_poll = result)
        else:
            html_response_str = render_template("error_pollenrolled_list.html", userid = userid)
    finally:
        if dbcursor is not None:
            dbcursor.close()

    return html_response_str


def doesPollExist(pollId):
    pollExists = False
    dbConnection = getdbconnection(mysqlconnection)
    dbcursor = None
    try:
        get_poll_query = "SELECT * FROM poll WHERE pollId = %s"
        dbcursor = dbConnection.cursor()
        dbcursor.execute(get_poll_query, (pollId))
        result = dbcursor.fetchone()
        if result != None:
            pollExists = True
    finally:
        dbcursor.close()

    return pollExists


def doesUserExist(userid):
    userExists = False
    dbConnection = getdbconnection(mysqlconnection)
    dbcursor = None
    try:
        get_user_query = "SELECT * FROM user WHERE userid = %s"
        dbcursor = dbConnection.cursor()
        dbcursor.execute(get_user_query, (userid))
        result = dbcursor.fetchone()
        if result != None:
            userExists = True
    finally:
        dbcursor.close()

    return userExists


def getdbconnection(con):
    if con is None or not con.open:
        con = pymysql.connect(user='2946161393',
                                      password='BBty48507701',
                                      host='2946161393.mysql.pythonanywhere-services.com',
                                      port=3306,
                                      database='2946161393$registration')

    return con


mysqlconnection = getdbconnection(None)

if __name__ == '__main__':
    app.run()