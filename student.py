'''
Project: WConnect 
Project Description: Mentor/Mentee Database for Wellesley Students
Authors: Adhel Geng and Soumaya Dammak
Course: CS304 Fall 2021

'''

from werkzeug.utils import secure_filename
import sys, os
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)

import cs304dbi as dbi
import bcrypt

import globalVars
#Input: cursor, conenciton, a string of the hobbies seperated by commas, and the user id
# seperates the hobbies, checks if the hobbies already exist in the hobby table and adds them if not. 
#It then adds the user the hobby to the hasHobby table
def processHobby(curs,hobbies,conn,nm):
    try:
        hobbies = hobbies.split(',')
        for hobby in hobbies:
            hobby = hobby.strip()
            try: 
                curs.execute(''' insert into hobby(name) values (%s)''',[hobby])
                conn.commit()
                curs.execute('select last_insert_id()')
                row = curs.fetchone()
                c = row[0]
            except Exception as error:
                curs.execute(''' select hb from hobby where name LIKE %s''', [hobby])
        
                c = curs.fetchone()[0]

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
        orga = orga.split()[0].strip()
        curs.execute(''' select clid from club where clubName LIKE %s''', ['%'+ orga+'%'])
        c = curs.fetchone()[0][0]
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

#processes the non required inputs 
def updateNonRequired(info,nm,conn,curs,app):
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
        processHobby(curs,hobbies,conn,nm)

    country = list(info.getlist("country"))
    org =list( info.getlist("org"))
    major = list(info.getlist("major"))

    #update the country table
    if len(country) != 0:
        processCountry(curs,country,conn,nm)
    
    #update the club table
    if len(org) != 0:
        processOrg(curs,org,conn,nm)
    #update the major table
    if len(major) != 0:
        processMajor(curs,major,conn,nm)
    
    #process image
    f = request.files['pic']
    processImage(f,nm,app,curs,conn)
    

#processes some of the required input 
def updateRequired(info,nm,conn,curs):
    curs.execute(''' update student set name = %s,mentor = %s,mentee = %s ,
    class = %s where nm = %s''',[info["name"],info["mentor"],info["mentee"],info["year"], nm])
    conn.commit()

# Input: connection and student id
# Output: the information of the given student 
def studentInfo(conn, id):
    curs = dbi.dict_cursor(conn)
    sql = "select * from student where nm = %s"
    curs.execute(sql,[id])
    info = curs.fetchone()
    # #major info
    sqlMajor = "select majorName from major inner join hasMajor using (mid) where nm = %s"
    curs.execute(sqlMajor,[id])
    vals = curs.fetchall()
    info["majors"] = [v["majorName"]for v in vals]
    # #race info
    sqlRace = "select * from student where race = %s"
    curs.execute(sqlRace,[id])
    vals = curs.fetchall()
    info["races"] = [v["race"]for v in vals]
    # #country info
    sqlCountry = "select name from country inner join fromCountry using (cid) where nm = %s"
    curs.execute(sqlCountry,[id])
    vals = curs.fetchall()
    info["country"] = [v["name"]for v in vals]
    # #org info
    sqlOrg = "select clubName from club inner join inClub using (clid) where nm = %s"
    curs.execute(sqlOrg,[id])
    vals = curs.fetchall()
    info["org"] = [v["clubName"]for v in vals]
    # #hobbies info
    sqlHobby = "select name from hobby inner join hasHobby where nm = %s"
    curs.execute(sqlHobby,[id])
    vals = curs.fetchall()
    info["hobbies"] = [v["name"]for v in vals]
    #careers info
    sqlCareer = "select career from student where nm = %s"
    curs.execute(sqlCareer,[id])
    vals = curs.fetchall()
    info["careers"] = [v["career"]for v in vals]
    return info

#Find all students
def allStudents(conn):
    """Returns the names of all students"""
    sql = "select * from student" 
    curs = dbi.dict_cursor(conn)
    curs.execute(sql)
    info = curs.fetchall()
    return info

#Filter students based on hobby
def filterByHobby(conn, hb):
    '''
    Returns the names and hobbies of people of the specified hobby
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select name from student inner join hasHobby using (nm) 
        where hb=%s''',[hb])
    return curs.fetchall()

#Filter students based on major
def filterByMajor(conn, mid):
    '''
    Returns the names of people of the specified major
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select name from student inner join hasMajor using (nm) 
        where mid=%s''',[mid])
    return curs.fetchall()

#Filter students based on class year
def filterByClass(conn):
    '''
    Returns the names of people of the specified class year
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select * from student where class=%s''')
    return curs.fetchall()

#Filter students based on whether or not one is a mentor
def filterByMentor(conn):
    '''
    Returns the names of people of who specified they were mentors
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select * from student where mentor=%s''')
    return curs.fetchall()

#Filter students based on whether or not one is a mentee
def filterByMentee(conn):
    '''
    Returns the names of people of who specified they were mentors
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select * from student where mentee=%s''')
    return curs.fetchall()

#Filter based on career interests
def filterByCareer(conn):
    '''
    Returns the names of people of the specified career
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select * from student where career=%s''')
    return curs.fetchall()

def login(conn, email, password):
    '''tries to log the user in given email & password. Returns True if
success and returns the uid as the second value on success.'''
    curs = dbi.cursor(conn)
    curs.execute('''SELECT nm, password FROM student WHERE email = %s''',
                 [email])
    row = curs.fetchone()
    if row is None:
        # no such user
        return (False, False)
    nm, hashed = row
    hashed2_bytes = bcrypt.hashpw(password.encode('utf-8'),
                                  hashed.encode('utf-8'))
    hashed2 = hashed2_bytes.decode('utf-8')
    if hashed == hashed2:
        return (True, nm)
    else:
        # password incorrect
        return (False, False)
