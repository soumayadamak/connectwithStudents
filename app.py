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
                flash(nm)
                columns = ["race","firstGen","spiritual","personality","immigration","city","bio","career"]
                final = []
                #update the student table
                for col in columns:
                    elt = info.getlist(col)
                    if elt == []:
                        elt = None
                    else:
                        elt = ','.join(elt)
                    final.append(elt)
                 
                final.append(nm)
                curs.execute(''' update student set race = %s, firstGen = %s, spiritual = %s,
                    personality = %s, immigration = %s, city = %s, bio = %s, career = %s where nm = %s''',final)
                conn.commit()
        
                hobbies = info["hobby"].strip().lower()
                #update the hobby tables
                if len(hobbies) != 0:
                    student.processHobby(curs,hobbies,conn,nm)

                country = list(info.getlist("country"))
                org =list( info.getlist("org"))
                major = list(info.getlist("major"))

                #update the country table
                if len(country) != 0:
                    student.processCountry(curs,country,conn,nm)
                
                #update the club table
                if len(org) != 0:
                    student.processOrg(curs,org,conn,nm)
                #update the major table
                if len(major) != 0:
                    student.processMajor(curs,major,conn,nm)

                #process image
                f = request.files['pic']
                student.processImage(f,nm,app,curs,conn)
                #redirect to home page 
                return redirect(url_for('index'))

            except Exception as err:
                flash('It failed  {}'.format(err))
                return render_template("createN.html", info = globalVars.info)



#Shows the basic navigation, ie the homepage, which will display all the users in the app (will later add the filter feature)
@app.route('/')
def index():
    """Landing page of WConnect"""
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute(''' select * from student''')
    students = curs.fetchall()
    return render_template('home.html', students = students, nm = session["uid"])


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



# @app.route("/pic/<profile>")
# def findPic(profile):
#     print("it got here")
#     return send_from_directory(app.config['UPLOADS'],profile)