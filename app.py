from flask import Flask, render_template, request, redirect, jsonify
# from database.db_connector import connect_to_database, execute_query
import os

# Configuration

app = Flask(__name__)

#global variable to store service choice
service_type = ''
zipcode_input = ''

# Routes 
@app.route('/')
def root():
	'''Return the homepage'''
	print('Root index hit. Redirecting to index.html...')
	return redirect('/index')

@app.route('/index')
def index():
    '''True URL of homepage'''
    print('Welcome to the homepage.')
    return render_template('index.html')

@app.route('/service_submission', methods=['POST'])
def service_submit():
	service_type = request.form["serviceType"]
	print("Service chosen =", service_type)
	return render_template('zipcode.html')

@app.route('/zipcode_submission', methods=['POST'])
def zipcode_submit():
	zipcode_input = request.form["inputZipcode"]
	print('Zipcode entered =', zipcode_input)
	return render_template('results.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8888)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port) 
