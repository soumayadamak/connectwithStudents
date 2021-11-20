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

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['UPLOADS'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# create account with required info only initially, the password check happens in the front end, will check the email there too
# when post and submit value is next , the user is added, a new session is created with user's id, email and logged in recorded 
# it then shows the second form of the non required information which will be handeled by same function but will just update 
@app.route('/create/', methods=['GET','POST'])
def create():
    if request.method == "GET":
        return render_template("createR.html", info = globalVars.info)
    else:
        info = request.form.copy()
        conn = dbi.connect()
        curs = dbi.cursor(conn)
        if info["submit"] == "Next":
            email = info["email"]
            pass1 = info["password1"]
            # if pass2 != pass1:
            #     flash ("passwords don't match")
            #     return render_template("createR.html", info = globalVars.info)
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
            return render_template( "create.html", info = globalVars.info)
        else: 
            try:
                nm = session['uid']
                print(info)
                columns = ["race","firstGen","spiritual","personality","immigration","city","bio","career"]
                final = []
                for col in columns:
                    final.append(info[col])
                    print(final)
                final.append(nm)
                curs.execute(''' update student set race = %s, firstGen = %s, spiritual = %s,
                 personality = %s, immigration = %s, city = %s, bio = %s, career = %s where nm = %s''',final)
                conn.commit()

                if len(info["hobby"]) != 0:
                    student.processHobby()
                if info["country"] != "NULL":
                    #process country 
                if info["org"] != "NULL":
                    #process org 
                if info["major"] != "NULL":
                    #process major

                allowed = {'jpg','gif','png'}
                #process image
                f = request.files['pic']
                user_filename = f.filename
                ext = user_filename.split('.')[-1]
                if ext not in allowed:
                    flash('extension not allowed, it needs to be jpg, gif, or png')
                    return render_template(create.html, info = globalVars.info)
                else:
                    filename = secure_filename('{}.{}'.format(nm,ext))
                    pathname = os.path.join(app.config['UPLOADS'],filename)
                    f.save(pathname)
                    curs.execute(''' update student set profile = %s ''',[filename])
                    conn.commit()
                #change the return here to redirect to user url?
                return render_template("base.html")

            except Exception as err:
                flash('Upload failed because {why}'.format(err))
                return render_template(create.html, info = globalVars.info)

        

# @app.route('/user/<username>')
# def user(username):
#     try:
#         # don't trust the URL; it's only there for decoration
#         if 'username' in session:
#             username = session['username']
#             uid = session['uid']
#             session['visits'] = 1+int(session['visits'])
#             return render_template('greet.html',
#                                    page_title='My App: Welcome {}'.format(username),
#                                    name=username,
#                                    uid=uid,
#                                    visits=session['visits'])
#         else:
#             flash('you are not logged in. Please login or join')
#             return redirect( url_for('index') )
#     except Exception as err:
#         flash('some kind of error '+str(err))
#         return redirect( url_for('index') )






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


# @app.route('/')
# def index():
#     return render_template('main.html',title='Hello')

# @app.route('/greet/', methods=["GET", "POST"])
# def greet():
#     if request.method == 'GET':
#         return render_template('greet.html', title='Customized Greeting')
#     else:
#         try:
#             username = request.form['username'] # throws error if there's trouble
#             flash('form submission successful')
#             return render_template('greet.html',
#                                    title='Welcome '+username,
#                                    name=username)

#         except Exception as err:
#             flash('form submission error'+str(err))
#             return redirect( url_for('index') )

# @app.route('/formecho/', methods=['GET','POST'])
# def formecho():
#     if request.method == 'GET':
#         return render_template('form_data.html',
#                                method=request.method,
#                                form_data=request.args)
#     elif request.method == 'POST':
#         return render_template('form_data.html',
#                                method=request.method,
#                                form_data=request.form)
#     else:
#         # maybe PUT?
#         return render_template('form_data.html',
#                                method=request.method,
#                                form_data={})



#log in page later 


# @app.route('/login/', methods=["POST"])
# def login():
#     username = request.form.get('username')
#     passwd = request.form.get('password')
#     conn = dbi.connect()
#     curs = dbi.dict_cursor(conn)
#     curs.execute('''SELECT uid,hashed
#                     FROM userpass
#                     WHERE username = %s''',
#                  [username])
#     row = curs.fetchone()
#     if row is None:
#         # Same response as wrong password,
#         # so no information about what went wrong
#         flash('login incorrect. Try again or join')
#         return redirect( url_for('index'))
#     stored = row['hashed']
#     print('LOGIN', username)
#     print('database has stored: {} {}'.format(stored,type(stored)))
#     print('form supplied passwd: {} {}'.format(passwd,type(passwd)))
#     hashed2 = bcrypt.hashpw(passwd.encode('utf-8'),
#                             stored.encode('utf-8'))
#     hashed2_str = hashed2.decode('utf-8')
#     print('rehash is: {} {}'.format(hashed2_str,type(hashed2_str)))
#     if hashed2_str == stored:
#         print('they match!')
#         flash('successfully logged in as '+username)
#         session['username'] = username
#         session['uid'] = row['uid']
#         session['logged_in'] = True
#         session['visits'] = 1
#         return redirect( url_for('user', username=username) )
#     else:
#         flash('login incorrect. Try again or join')
#         return redirect( url_for('index'))


#logout : later

# @app.route('/logout/')
# def logout():
#     if 'username' in session:
#         username = session['username']
#         session.pop('username')
#         session.pop('uid')
#         session.pop('logged_in')
#         flash('You are logged out')
#         return redirect(url_for('index'))
#     else:
#         flash('you are not logged in. Please login or join')
#         return redirect( url_for('index') )