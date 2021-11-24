#from _typeshed import IdentityFunction
from flask import (Flask, url_for, render_template)
import cs304dbi as dbi
app = Flask(__name__)

# insert person into database
def insert(conn, id, name, email, password):
    sql = "INSERT INTO student(id, name, email, password) VALUES(%s, %s, %s, %s)" 
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,[id, name, email, password]) 
    conn.commit()
    return

# update/edit student with new information
def edit(conn, OLDid, NEWid, name, email, password):
    sql = "UPDATE student SET id= %s, name = %s, email = %s, password = %s WHERE id = %s" 
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,[NEWid, name, email, password,OLDid]) 
    conn.commit()
    return

# find all students   
def findStudent(conn):
    sql = "select name from student where id = %s" 
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,[id])
    info = curs.fetchall()
    return info

# find a single student
def studentInfo(conn, id):
    sql = "select * from student where id = %s"
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,[id])
    info = curs.fetchone()
    return info

def view(conn,id):
    sql = dbi.dict_cursor(conn)
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,[id]) 
    conn.commit()
    return


if __name__ == '__main__':
    dbi.cache_cnf()   
    dbi.use('ageng_db')
    conn = dbi.connect()