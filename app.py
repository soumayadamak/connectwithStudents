from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)


import bcrypt
import cs304dbi as dbi
# import cs304dbi_sqlite3 as dbi

#contains global variables needed to make the account form 
import globalVars 

#contains supporting functions
import student
import random

# replace that with a random key
app.secret_key = 'secret'


# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['UPLOADS'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# create account with required info only initially, the password check happens in the front end
# when post and submit value is next , the user is added, a new session is created with user's id, email and logged in recorded 
# it then shows the second form of the non required information which will be handeled by same function but will just update 
#after the non required information is processed, it redirects to the home page 
@app.route('/create/', methods=['GET','POST'])
def create():

    if request.method == "GET":
        return render_template("createR.html", info = globalVars.info)
    else:

        info = request.form.copy()
        conn = dbi.connect()
        curs = dbi.cursor(conn)
        #process the required information 
        if info["submit"] == "Next":
            email = info["email"]
            pass1 = info["password1"]
            hashed = bcrypt.hashpw(pass1.encode('utf-8'),
                            bcrypt.gensalt())
            stored = hashed.decode('utf-8')
            try:
                
                curs.execute('''INSERT INTO student(name,email,password,mentor,mentee,class)
                                VALUES(%s,%s,%s,%s,%s,%s)''',
                            [info["name"],email,stored,info["mentor"],info["mentee"],info["year"]])
                conn.commit()
            except Exception as err:
                flash('That username is taken: {}'.format(repr(err)))
                return render_template("createR.html", info = globalVars.info)
            curs.execute('select last_insert_id()')
            row = curs.fetchone()
            uid = row[0]
            session['email'] = email
            session['uid'] = uid
            session['logged_in'] = True
            session['visits'] = 1
            return render_template( "createN.html", info = globalVars.info)
        else: 
            try:
               #process non required information
                nm = session['uid']
                student.updateNonRequired(info,nm,conn,curs,app)
                return redirect(url_for('index'))
            except Exception as err:
                flash('It failed  {}'.format(err))
                return render_template("createN.html", info = globalVars.info)


@app.route('/edit/', methods = ['Get','POST'])
def edit():
    if request.method == "GET":
        conn = dbi.connect()
        s = student.studentInfo(conn, session["uid"])
        for col in s:
            if s[col] == None:
                s[col] = []
        s["majors"] = []
        s["races"] = []
        s["country"] = []
        s["org"] = []
        s["hobbies"] = ','.join(["test","test"])
        print(s)
        return render_template("edit.html", student = s, info = globalVars.info, nm = session["uid"])
    else:
        info = request.form.copy()
        nm = session['uid']
        conn = dbi.connect()
        curs = dbi.cursor(conn)
        student.updateNonRequired(info,nm,conn,curs,app)
        student.updateRequired(info,nm,conn,curs)
        return redirect(url_for('index'))

#Shows the basic navigation, ie the homepage, which will display all the users in the app (will later add the filter feature)
@app.route('/')
def index():
    if 'logged_in' in session:
        """Landing page of WConnect"""
        conn = dbi.connect()
        curs = dbi.dict_cursor(conn)
        curs.execute(''' select * from student''')
        students = curs.fetchall()
        
        for student in students: 
            if student.get("profile") == None:
                student["profile"] = 'default.jpg'
            student["src"] = url_for('findPic', profile = student.get("profile"))
        return render_template('home.html', students = students, nm = session["uid"])
    else:
        return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    """resets logged_in, uid and email keys of the session and redirects to the log in url """
    session.pop('logged_in')
    session.pop('uid')
    session.pop('email')
    return redirect(url_for('login'))
    
@app.route('/login/', methods=['GET','POST'])
def login():
    """Diplays the log in page or processes the log in information. Returns 
    the home page if the user already logged in or logs in successfully and returns
    the log in page if the log in information is not correct """
    if request.method == "GET":
        #if user already logged in 
        if 'logged_in' in session:
            flash("already logged in")
            return redirect(url_for('index'))
        else:
            #user not logged in yet 
            return render_template("login.html")
    else:
        info = request.form
        email = info["email"].strip()
        password = info["password"]
        conn = dbi.connect()
        logged, nm = student.login(conn, email, password)
        if logged:
            session['logged_in'] = True
            session['visits'] += 1
            session['uid'] = nm
            session['email'] = email
            return redirect(url_for('index'))
        else:
            flash("Wrong password")
            return render_template("login.html")

        
            
#main page 
@app.route('/findamentor/')
def findMentor():
    #will be implemented later
    """Main interaction page where mentors/mentees find each other"""
    return render_template("findMentor.html", nm = session["uid"])


#Shows the student profile when the "view" button is clicked
@app.route('/profile/<id>', methods=['GET','POST'])
def view(id):
    conn = dbi.connect()
    user = student.studentInfo(conn, id)
    return render_template("account.html", nm = session["uid"], student = user)


@app.route("/pic/<profile>")
def findPic(profile):
    print("it got here")
    return send_from_directory(app.config['UPLOADS'],profile)


@app.before_first_request
def init_db():
    dbi.cache_cnf()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'sdammak_db' 
    dbi.use(db_to_use)
    print('will connect to {}'.format(db_to_use))

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)



