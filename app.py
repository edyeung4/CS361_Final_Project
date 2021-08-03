from flask import Flask, render_template, request, redirect, jsonify
# from database.db_connector import connect_to_database, execute_query
import os
from gmaps_scraper import WebDriver

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
	global service_type
	service_type = request.form["serviceType"]
	print("Service chosen =", service_type)
	print(service_type)
	return render_template('zipcode.html')

@app.route('/zipcode_submission', methods=['POST'])
def zipcode_submit():
	global service_type
	zipcode_input = request.form["inputZipcode"]
	print('Zipcode entered =', zipcode_input)
	# print(service_type)
	gmaps_scraper = WebDriver()
	results = gmaps_scraper.scrape(service_type, zipcode_input)
	print(results)

	return render_template('results.html', service=service_type, name_bizDescrip=zip(results['name'], results['business_descrip']))

@app.route('/service_selection', methods=['POST'])
def service_select():
	global service_type
	name = request.form['name']
	descrip = request.form['descrip']
	print(name)
	# print('hello')
	return render_template('results_final.html', service=service_type, name=name, descrip=descrip)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8888)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port) 
