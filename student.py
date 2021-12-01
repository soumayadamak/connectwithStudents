from werkzeug.utils import secure_filename
import sys, os
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)

import cs304dbi as dbi
def processHobby(curs,hobbies,conn,nm):
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

def processCountry(curs,country,conn,nm):
    for coun in country:
        coun = coun.split()[0]
        curs.execute(''' select cid from country where name LIKE %s''', ['%'+coun+'%'])
        c = curs.fetchall()[0][0]
        curs.execute(''' insert into fromCountry(nm,cid) values (%s,%s)''',[nm,c])
        conn.commit()    

def processOrg(curs,org,conn,nm):
    for orga in org: 
    
        orga = orga.split()[0]
        curs.execute(''' select clid from club where clubName LIKE %s''', ['%'+orga.strip()+'%'])
        c = curs.fetchall()[0][0]
        curs.execute(''' insert into inClub(nm,clid) values (%s,%s)''',[nm,c])
        conn.commit()
def processMajor(curs,major,conn,nm):
    for maj in major:
        maj = maj.split()[0]
        curs.execute(''' select mid from major where majorName LIKE %s''', ['%'+maj+'%'])        
        c = curs.fetchall()[0][0]
        curs.execute(''' insert into hasMajor(nm,mid) values (%s,%s)''',[nm,c])
        conn.commit()
def processImage(f,nm,app,curs,conn):
    allowed = {'jpg','gif','png'}
                
    user_filename = f.filename
    ext = user_filename.split('.')[-1]
    if ext == '':
        
        curs.execute(''' update student set profile = %s ''',['default.jpg'])
        conn.commit()
       

    if ext not in allowed:
        flash('extension not allowed, it needs to be jpg, gif, or png')
        return render_template("createN.html", info = globalVars.info)
    else:
        filename = secure_filename('{}.{}'.format(nm,ext))
        pathname = os.path.join(app.config['UPLOADS'],filename)
        f.save(pathname)
        curs.execute(''' update student set profile = %s ''',[filename])
        conn.commit()



# find a single student
def studentInfo(conn, id):
    curs = dbi.dict_cursor(conn)
    sql = "select * from student where nm = %s"
    curs.execute(sql,[id])
    info = curs.fetchone()
    return info
