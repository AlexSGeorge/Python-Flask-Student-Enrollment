import sqlite3 
import random
from datetime import datetime

dbname = 'customers.db'


def totRecords():
    # Assume no errors, can add try except blocks
    con = sqlite3.connect(dbname)
    curs = con.cursor()
    curs.execute('SELECT COUNT(*) FROM customer')
    record = curs.fetchall()
    con.close()
    return record[0][0]

def recProcessed():
    # Assume no errors, can add try except blocks
    con = sqlite3.connect(dbname)
    curs = con.cursor()
    curs.execute('SELECT COUNT(*)')
    record = curs.fetchall()
    con.close()
    return record[0][0]

def allRecords():
    con = sqlite3.connect(dbname)
    curs = con.cursor()
    curs.execute('SELECT COUNT(*) FROM customer')
    record = curs.fetchall()
    con.close()
    return record

def reports(id):
    if id == '1':
        sqlCmd = """ SELECT *
                     FROM customer 
                     ORDER BY cusLname"""
    if id == '2':
        sqlCmd = """ SELECT *
                     FROM customer 
                     ORDER BY cusSalesYTD DESC"""
    if id == '3':
        sqlCmd = """SELECT *
                    FROM customer
                    ORDER BY random()
                    LIMIT 3
                    """

    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()

    try:
        curs.execute(sqlCmd)
        records = curs.fetchall()

    except Exception as e:
        return 'error ' + str(e)
    
    else:
        return records

    finally:
        con.close()



def findCustomers(pDict):
    sqlCmd = "1 = 1"
    if pDict['cusId'] != '':
        sqlCmd += " and upper(cusId) = " + pDict['cusId'].upper()
    if pDict['cusFname'] != '':
        sqlCmd += " and upper(cusFname) like '" + pDict['cusFname'].upper() + "%'"
    if pDict['cusLname'] != '':
        sqlCmd += " and upper(cusLname) like '" + pDict['cusLname'].upper() + "%'"
    if pDict['cusState'] != '':
        sqlCmd += " and upper(cusState) like '" + pDict['cusState'].upper() + "%'"
    if pDict['cusSalesYTD'] != '':
        sqlCmd += " and upper(cusSalesYTD) like '" + pDict['cusSalesYTD'].upper() + "%'"
    if pDict['cusSalesPrev'] != '':
        sqlCmd += ' and cusSalesPrev >= ' + pDict['cusSalesPrev']
    
    sqlCmd = 'SELECT * FROM customer WHERE ' + sqlCmd

    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()
    try:
        curs.execute(sqlCmd)
        record = curs.fetchall()
        return record    
    except Exception as e:
        return ('Error ' + str(e))
    finally:
        con.close()


def findCustomerById(cusId):
    sqlCmd = 'SELECT * FROM customer WHERE cusId = ?'

    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()
    try:
        curs.execute(sqlCmd, (cusId,))
        record = curs.fetchall()
    except Exception as e:
        return ('Error ' + str(e))
    else:
        return record    
    finally:
        con.close()   

def deleteCustomerById(cusId):
    sqlCmd = 'DELETE FROM customer WHERE cusId = ?'
    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()
    try:
        curs.execute(sqlCmd, (cusId,))
        rowcount = curs.rowcount
        con.commit()
    except Exception as e:
        return ('Error ' + str(e))
    else:
        return rowcount   
    finally:
        con.close()   
        
def updateCustomer(pDict):
    con = sqlite3.connect(dbname)
    curs = con.cursor()
    try:
        sqlCmd = """UPDATE customer 
                    SET cusFname = ?, cusLname = ?, cusState = ?, cusSalesYTD = ?, cusSalesPrev = ?
                    WHERE cusId = ?"""
        curs.execute(sqlCmd, (pDict['cusFname'], pDict['cusLname'],pDict['cusState'], float(pDict['cusSalesYTD']), float(pDict['cusSalesPrev']), int(pDict['cusId'])))
        rowcount = curs.rowcount
        con.commit()
    except Exception as e:
        return ('Error ' + str(e))
    else:
        return rowcount
    finally:
        con.close()

def sql_insert_customer(collection, errfile):
    con = sqlite3.connect(dbname)
    curs = con.cursor()

    try:
        curs.execute('INSERT INTO customer(cusId, cusFname, cusLname, cusState, cusSalesYTD, cusSalesPrev) VALUES(?,?,?,?,?,?)', collection)
    except sqlite3.IntegrityError as e:
        with open(errfile, mode ='a') as errorfile:
            for item in collection:
                print(item, end=' ', file = errorfile)
            print(file=errorfile)
        return 'Error' + str(e)
    except Exception as e:
        print('exception', str(e))
        return 'Error' + str(e)
    con.commit()
    return "Success"

def insert_customer(collection):
    con = sqlite3.connect(dbname)
    curs = con.cursor()
    try:
        curs.execute('INSERT INTO customer(cusId, cusFname, cusLname, cusState, cusSalesYTD, cusSalesPrev) VALUES(?,?,?,?,?,?)', collection)
    except sqlite3.IntegrityError as e:
        return 'Error' + str(e)
    except Exception as e:
        return'Error' + str(e)
    con.commit()
    return 'Success'\


def export_customer(cusId):
    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()
    sqlCmd = """SELECT * 
                FROM customer"""
    curs.execute(sqlCmd);
    records = curs.fetchall()
        
    with open ('testfile.txt', mode='w') as tstFile:
        for customer in records:
            print(customer['cusId'], customer['cusFname'], customer['cusLname'], customer['cusState'], customer['cusSalesYTD'], customer['cusSalesPrev'], file = tstFile)
    con.commit()
    con.close()
