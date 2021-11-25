from werkzeug.utils import secure_filename
import sys, os
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)

import cs304dbi as dbi

#Input: cursor, conenciton, a string of the hobbies seperated by commas, and the user id
# seperates the hobbies, checks if the hobbies already exist in the hobby table and adds them if not. 
#It then adds the user the hobby to the hasHobby table
def processHobby(curs,hobbies,conn,nm):
    try:
        hobbies = hobbies.split(',')
        for hobby in hobbies:
            hobby = hobby.strip()
            curs.execute(''' select hb from hobby where name LIKE %s''', ['%'+hobby+'%'])
            c = curs.fetchall()
            if len(c) == 0 :
                curs.execute(''' insert into hobby(name) values (%s)''',[hobby])
                conn.commit()
                curs.execute('select last_insert_id()')
                row = curs.fetchone()
                c = row[0]
            curs.execute(''' insert into hasHobby(nm,hb) values (%s,%s)''',[nm,c])
            conn.commit()
    except Exception as err:
        flash('The hobbies are not seperated by commas: {}'.format(repr(err)))
        return render_template("createN.html", info = globalVars.info)

#Input: cursor, connection, a list of the countries and user id
# Loops through the countries that the user selected and adds each country to the fromCountry table

def processCountry(curs,country,conn,nm):
    for coun in country:
        coun = coun.split()[0]
        curs.execute(''' select cid from country where name LIKE %s''', ['%'+coun+'%'])
        c = curs.fetchall()[0][0]
        curs.execute(''' insert into fromCountry(nm,cid) values (%s,%s)''',[nm,c])
        conn.commit()    
#Input: cursor, connection, a list of the clubs and user id
# Loops through the clubs that the user selected and adds each club to the inClub table
def processOrg(curs,org,conn,nm):
    for orga in org: 
        orga = orga.split()[0]
        curs.execute(''' select clid from club where clubName LIKE %s''', ['%'+orga.strip()+'%'])
        c = curs.fetchall()[0][0]
        curs.execute(''' insert into inClub(nm,clid) values (%s,%s)''',[nm,c])
        conn.commit()

#Input: cursor, connection, a list of the majors and user id
# Loops through the majors that the user selected and adds each major to the hasMajor table
def processMajor(curs,major,conn,nm):
    for maj in major:
        maj = maj.split()[0]
        curs.execute(''' select mid from major where majorName LIKE %s''', ['%'+maj+'%'])        
        c = curs.fetchall()[0][0]
        curs.execute(''' insert into hasMajor(nm,mid) values (%s,%s)''',[nm,c])
        conn.commit()

#Input: cursor, connections,user id, the flask app, and the file object
# checks if the user selected an image. If not, it assigns the default image to them 
#If yes, it checks if the image is in the allowed extensions or not. If not, it renders the form again
#If  yes, it stores the image in the student table and saves it in the uploads 
def processImage(f,nm,app,curs,conn):
    allowed = {'jpg','gif','png'}
   
    user_filename = f.filename
    ext = user_filename.split('.')[-1]
    if ext == '':
        curs.execute(''' update student set profile = %s  where nm = %s''',['default.jpg',nm])
        conn.commit()
    elif ext not in allowed:
        flash('extension not allowed, it needs to be jpg, gif, or png')
        return render_template("createN.html", info = globalVars.info)
    else:
        name = secure_filename('{}.{}'.format(nm,ext))
        pathname = os.path.join(app.config['UPLOADS'],name)
        f.save(pathname)
        curs.execute(''' update student set profile = %s where nm = %s''',[name,nm])
        conn.commit()

# Input: conenction and stduent id
# Output: the information of the given student 
def studentInfo(conn, id):
    curs = dbi.dict_cursor(conn)
    sql = "select * from student where nm = %s"
    curs.execute(sql,[id])
    info = curs.fetchone()
    return info
