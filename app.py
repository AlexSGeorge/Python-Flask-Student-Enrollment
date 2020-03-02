from flask import Flask, render_template, request
import sqlite3 
import dbtasks

app = Flask(__name__)
dbname = 'customers.db'

@app.route('/', methods = ['POST', 'GET'])
@app.route('/customers', methods = ['POST', 'GET'])
def customers():
   if request.method == 'GET':
      totRec = dbtasks.totRecords()
      customer = {}
      return render_template('customers.html', totRec=totRec, customer=customer)  

   if request.method == 'POST':
      source = 'post'
      totRec = dbtasks.totRecords()
      customer = request.form
      cusRecords = dbtasks.findCustomers(customer)

      return render_template('customers.html', totRec=totRec, customer=customer, cusRecords=cusRecords, source=source)  


@app.route('/delete/<cusId>', methods = ['POST', 'GET'])
def delete(cusId):
    if request.method == 'GET':
        customer = dbtasks.findCustomerById(cusId)
        return render_template('delete.html', customer=customer)

    if request.method == 'POST':
        customer = request.form
        msg = dbtasks.deleteCustomerById(cusId)
        if msg == 1:
            message = 'Customer Deleted Successfully'
        else:
            message = 'Error Deleting Customer.  Error: ' + msg
            
        return render_template('message.html', message=message)      


@app.route('/update/<cusId>', methods = ['POST', 'GET'])
def update(cusId):
    if request.method == 'GET':
        source = 'GET'
        customer = dbtasks.findCustomerById(cusId)
        return render_template('update.html', source=source, customer=customer)

    if request.method == 'POST':
        source = 'POST'
        customer = request.form
        msg = dbtasks.updateCustomer(customer)
        if msg == 1:
           message = 'Customer Updated Successfully'
           return render_template('message.html', message=message, customer=customer)  
        else:
           message = 'Error Updating Customer.  Message: ' + msg
           return render_template('update.html', message=message, customer=customer) 

@app.route('/', methods = ['POST', 'GET'])
@app.route('/reports', methods = ['POST', 'GET'])
def reports():
    if request.method == 'GET':
        source = 'GET'
        report = {}
        totRec = dbtasks.totRecords()
        return render_template('reports.html', source=source, report=report, totRec=totRec)

    if request.method == 'POST':
        source = 'POST'
        report = request.form
        result = dbtasks.reports(report['report'])
        return render_template('reports.html', source=source, report=report, result=result)

@app.route('/addcustomer')
def addcustomer():
    if request.method == 'GET':
        source = 'GET'
        customer = {}
        return render_template('addcustomer.html', source = source, customer = customer)


@app.route('/addcustomerresults', methods = ['POST', 'GET'])
def addcustomerresults():
    if request.method == 'POST':
        source = 'post'
        customer = request.form
        status = dbtasks.insert_customer(customer)
        return render_template("addcustomerresults.html", customer = customer, status=status)


@app.route('/import_filenames')
def input_filenames():
    return render_template('import_filenames.html')

@app.route('/import_fileprocess', methods = ['POST', 'GET'])
def result_fileprocess():
    if request.method == 'GET':
        source = 'GET'
        report = {}
        totRec = dbtasks.totRecords()
        recProc = dbtasks.recProcessed()
        allRec = dbtasks.allRecords()
        return render_template('import_fileprocess.html', source=source, report=report, totRec=totRec, recProc=recProc, allRec=allRec)
    
    if request.method == 'POST':
        files = request.form
        txtfile = files['txtfile']
        errorfile = 'input_error.txt'
        status = 'Success'

        with open(txtfile, mode='r') as customerfile:
            for record in customerfile:
                rec = record.split()
                msg = dbtasks.sql_insert_customer(rec, errorfile)
                if msg != 'Success':
                    status = msg
        return render_template('import_fileprocess.html', status = status, errorfile = errorfile)

#Select *
#from customer
@app.route('/export_filenames')
def export_filenames():
    return render_template('export_filenames.html')


@app.route('/export_fileprocess', methods = ['POST', 'GET'])
def export_fileprocess():
    if request.method == 'POST':
        source = 'post'
        customer = request.form
        status = dbtasks.export_customer(customer)
        return render_template("export_fileprocess.html", source = source, customer = customer, status=status)

if __name__ == '__main__':
      app.run(debug = True)